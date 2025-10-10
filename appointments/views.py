from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Booking
from .forms import BookingForm
from datetime import datetime, timedelta, date
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.utils.safestring import mark_safe
from .utils import Calendar
import calendar  # python standard calendar
from .services.mailer import send_booking_invite
from django.db.models import Q
from appointments.filters import BookingFilter
from django.shortcuts import get_object_or_404
from django.utils.timezone import make_aware, get_current_timezone, is_aware

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from django.http import FileResponse
import io

def create_booking(request):
    if request.method == "POST":
        form = BookingForm(request.POST, current_user=request.user)
        if form.is_valid():
            # Don't save the booking before checking for conflicts
            booking = form.save(commit=False)
            booking.booked_by = request.user

            # get all selected participants from form
            participants = form.cleaned_data["participants"]

            # checks, if participants are already booked at that time
            conflicts = booking.is_conflicting(participants=participants)
            if conflicts:
                conflicts_names = ", ".join(
                    [str(participant) for participant in conflicts]
                )
                messages.error(
                    request,
                    (f"Find another timeslot, as {conflicts_names}"
                     f" is/are already booked."),
                )
                # form not valid so render the form again
                return render(
                    request, "appointments/booking_create.html", {"form": form}
                )

            """ if form is valid and no conflict found
            1. save booking,
            2. save m2m relations ("participants)
            3. send e-mail ics.file to all participants
            4. show success message"""
            booking.save()
            form.save_m2m()
            recipients = [
                participant.email for participant in booking.participants.all()
            ]
            send_booking_invite(booking, recipients)
            messages.success(request, "Booking was succesfull")

    else:
        form = BookingForm(current_user=request.user)

    return render(request, "appointments/booking_create.html", {"form": form})


@login_required
def booking_list(request):
    # all bookings where current-user has created or is participants
    current_user = request.user
    bookings = (
        Booking.objects.filter(Q(booked_by=current_user) |
                               Q(participants=current_user))
        .distinct()
        .order_by("-created_at")
    )

    # use filter from queryset
    booking_filter = BookingFilter(request.GET, queryset=bookings)
    bookings = booking_filter.qs

    # define timeframe (e.g. next month)
    today = date.today()
    start_date = today - timedelta(days=7)
    end_date = today + timedelta(days=30)

    # list all bookings and recurrence bookings
    expanded_bookings = []
    tz = get_current_timezone()

    for booking in bookings:
        if booking.recurrence != "none":
            occurrences = booking.get_occurrences(start_date, end_date)
            for occ_start in occurrences:
                duration = booking.end - booking.start
                occ_end = occ_start + duration

                # ensure aware
                if not is_aware(occ_start):
                    occ_start = make_aware(occ_start, tz)
                if not is_aware(occ_end):
                    occ_end = make_aware(occ_end, tz)

                # save all references for expanded-bookings
                expanded_bookings.append({
                    "booking": booking,
                    "occurrence": occ_start,
                    "end_occurrence": occ_end
                })
        else:
            start = booking.start
            end = booking.end
            if not is_aware(start):
                start = make_aware(start, tz)
            if not is_aware(end):
                end = make_aware(end, tz)
            expanded_bookings.append({
                "booking": booking,
                "occurrence": start,
                "end_occurrence": end
            })

    # sort chronologically
    expanded_bookings.sort(key=lambda x: x["occurrence"])

    context = {"bookings": expanded_bookings,
               "filter": booking_filter}

    return render(request, "appointments/booking_list.html", context)


# ---print booking_list to pfd.file ---


@login_required
def booking_pdf(request):
    """ Create a PDF file from booking_list with all/expanded bookings
        for the logged in users appointments"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        rightMargin=30, leftMargin=30,
        topMargin=30, bottomMargin=18,
    )

    elements = []
    styles = getSampleStyleSheet()
    title = Paragraph("Appointment List", styles["Title"])
    elements.append(title)
    elements.append(Spacer(1, 12))

    current_user = request.user

    bookings = (
        Booking.objects.filter(Q(booked_by=current_user) | Q(participants=current_user))
        .distinct()
        .order_by("-created_at")
    )

    booking_filter = BookingFilter(request.GET, queryset=bookings)
    bookings = booking_filter.qs

    today = date.today()
    start_date = today - timedelta(days=7)
    end_date = today + timedelta(days=30)
    tz = get_current_timezone()

    expanded_bookings = []

    for booking in bookings:
        if booking.recurrence != "none":
            occurrences = booking.get_occurrences(start_date, end_date)
            for occ_start in occurrences:
                duration = booking.end - booking.start
                occ_end = occ_start + duration

                if not is_aware(occ_start):
                    occ_start = make_aware(occ_start, tz)
                if not is_aware(occ_end):
                    occ_end = make_aware(occ_end, tz)

                expanded_bookings.append({
                    "title": booking.title,
                    "occurrence": occ_start,
                    "end_occurrence": occ_end,
                    "status": booking.status,
                    "participants": ", ".join([str(p) for p in booking.participants.all()]),
                })
        else:
            start = booking.start
            end = booking.end
            if not is_aware(start):
                start = make_aware(start, tz)
            if not is_aware(end):
                end = make_aware(end, tz)
            expanded_bookings.append({
                "title": booking.title,
                "occurrence": start,
                "end_occurrence": end,
                "status": booking.status,
                "participants": ", ".join([str(p) for p in booking.participants.all()]),
            })

    # Sort chronologically by start time
    expanded_bookings.sort(key=lambda x: x["occurrence"])

    # --- Create table ---
    data = [["Title", "Start", "End", "Status", "Participants"]]

    for eb in expanded_bookings:
        data.append([
            eb["title"],
            eb["occurrence"].strftime("%Y-%m-%d %H:%M"),
            eb["end_occurrence"].strftime("%Y-%m-%d %H:%M"),
            eb["status"],
            eb["participants"],
        ])

    # --- Format pdf table ---
    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.beige]),
    ]))

    elements.append(table)
    doc.build(elements)
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename="booking_list.pdf")



@login_required
def edit_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, booked_by=request.user)

    if request.method == "POST":
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect("appointments:booking_list")
    else:
        form = BookingForm(instance=booking)
    return render(request, "appointments/booking_edit.html", {"form": form})


@login_required
def delete_booking(request, pk):
    booking = Booking.objects.get(pk=pk)
    if request.method == "POST":
        booking.delete()
        return redirect("appointments:booking_list")
    return render(request,
                  "appointments/booking_delete.html",
                  {"booking": booking})


# -- Calendar --

class CalendarView(LoginRequiredMixin, generic.ListView):
    model = Booking
    template_name = "appointments/calendar.html"

    """create context-dict =
                        {"object_list":"[]",
                         "prev-month": "",
                         "next-month":"",
                         calendar:""} """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date/month for the calendar
        d = get_date(self.request.GET.get("month", None))
        context["prev_month"] = prev_month(d)
        context["next_month"] = next_month(d)

        # timeframe: full month
        first_day = d.replace(day=1)
        last_day = first_day + timedelta(
            days=calendar.monthrange(d.year, d.month)[1] - 1
        )

        # get all bookings
        bookings = Booking.objects.all()

        # list of occurences
        expanded_events = []
        for booking in bookings:
            occurrences = booking.get_occurrences(first_day, last_day)
            for occ in occurrences:
                expanded_events.append((occ, booking))

        # Instantiate our calendar class with today's year, date and occurences
        cal = Calendar(d.year, d.month, events=expanded_events)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context["calendar"] = mark_safe(html_cal)
        return context


def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split("-"))
        return date(year, month, day=1)
    return datetime.today().date()


def prev_month(d):
    first = d.replace(day=1)
    prev = first - timedelta(days=1)
    return f"month={prev.year}-{prev.month}"


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    nxt = last + timedelta(days=1)
    return f"month={nxt.year}-{nxt.month}"
