from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.utils.safestring import mark_safe
from django.core.mail import EmailMessage
from django.http import FileResponse
from datetime import datetime, timedelta, date
from django.utils.timezone import localtime
from appointments.services.ics_generator import generate_ics
import calendar
import io

from .models import Booking, BookingInstance
from .forms import BookingForm, BookingInstanceEditForm
from appointments.filters import BookingInstanceFilter
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle,
                                Paragraph, Spacer)
from reportlab.lib.styles import getSampleStyleSheet
from .utils import Calendar


# -----------------------------
# Create Booking 
# -----------------------------
def create_booking(request):
    if request.method == "POST":
        form = BookingForm(request.POST, current_user=request.user)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.booked_by = request.user

            participants = form.cleaned_data["participants"]
            conflicts = booking.is_conflicting(participants=participants)
            if conflicts:
                names = ", ".join(str(p) for p in conflicts)
                messages.error(
                    request,
                    (f"Find another timeslot, as {names}"
                     f" is/are already booked."))
                return render(request, "appointments/booking_create.html",
                              {"form": form})

            booking.save()
            booking.generate_booking_instances()
            form.save_m2m()
            messages.success(request, "Booking was successful")
            return redirect("appointments:booking")
    else:
        form = BookingForm(current_user=request.user)

    return render(request, "appointments/booking_create.html", {"form": form})

# -----------------------------
# Booking List (Day / Week View)
# -----------------------------
@login_required
def booking_list(request):
    current_user = request.user

    instances = BookingInstance.objects.filter(
        Q(booking__booked_by=current_user) |
        Q(booking__participants=current_user),
    ).filter(is_cancelled=False).distinct()

    # Filter via GET parameters
    instance_filter = BookingInstanceFilter(request.GET, queryset=instances)
    filtered_instances = instance_filter.qs.order_by("start")

    context = {
        "bookings": filtered_instances,
        "filter": instance_filter
    }
    return render(request, "appointments/booking_list.html", context)

# -----------------------------
# Booking Edit single Instances
# -----------------------------
@login_required
def edit_booking_instance(request, booking_id, instance_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    instance = get_object_or_404(
        BookingInstance, pk=instance_id, booking=booking)

    if request.method == "POST":
        form = BookingInstanceEditForm(request.POST, instance=instance)
        if form.is_valid():
            inst = form.save(commit=False)
            inst.is_modified = True

        new_status = form.cleaned_data.get("status")

        # Status can only be changed by one time bookings
        if booking.recurrence == "none":
            if new_status and new_status != booking.status:
                booking.status = new_status
                booking.save()
        else:
            messages.warning(
                request,
                "Info: Status changes are only possible for one-time bookings."
                " Recurring events need to be cancelled or deleted by the"
                " creator."
            )

        # check appointment-conflicts before saving
        conflicts = inst.booking.is_conflicting(
            participants=inst.booking.participants.all(),
            instance=inst
        )
        if conflicts:
            messages.error(
                request,
                "Cannot update instance due to conflicts with: "
                + ", ".join(
                    [p.username if p.username else str(p)
                        for p in conflicts if p is not None]
                )
            )
            return redirect(
                "appointments:booking_instance_edit",
                booking_id=booking.id,
                instance_id=inst.id
                    )
        # save instance if no conflicts
        inst.occurrence_date = inst.current_start.date()
        inst.save()
        messages.success(request,
                         (f"Appointment on {inst.occurrence_date}"
                          f" is updated successfully."))

    else:
        form = BookingInstanceEditForm(instance=instance, booking=booking)

    context = {
        "form": form,
        "instance": instance,
        "booking": booking,
    }
    return render(request, "appointments/booking_instance_edit.html", context)


# -----------------------------
# Delete Booking / Instance
# -----------------------------
@login_required
def delete_booking(request, pk, instance_id=None):
    """A deletion can only be done by the creator,
        and a permanent deletion is only possible,
        if the recurrence is none or all recurring instances are cancelled
        If the booking or instance does not exist, the user is redirected with
        a warning."""
    try:
        booking = Booking.objects.get(pk=pk)
    except Booking.DoesNotExist:
        messages.warning(request,
                         "The booking you tried to access does not exist.")
        # return redirect("appointments:booking_list")

    # only creator is allowed to delete
    if booking.booked_by != request.user:
        name = booking.booked_by.get_full_name() or booking.booked_by.username
        messages.warning(
            request,
            f"Sorry, only the appointment creator ({name}) "
            f"is allowed to delete this appointment.")
        return render(
            request,
            "appointments/booking_delete.html",
            {"booking": booking}
        )

    instance = None
    if instance_id:
        try:
            instance = BookingInstance.objects.get(
                id=instance_id, booking=booking)
        except BookingInstance.DoesNotExist:
            messages.warning(
                request,
                "This occurrence was already deleted or does not exist."
            )
            # return redirect("appointments:booking_list")

    if request.method == "POST":
        if instance:
            if booking.recurrence != "none":
                # Cancel only individual instances
                instance.is_cancelled = True
                instance.save()
                messages.success(
                    request,
                    f"The occurrence on {instance.occurrence_date}"
                    f" was cancelled.")
                if not booking.all_booking_instances.filter(is_cancelled=False).exists():
                    booking.delete()
                    messages.info(
                        request,
                        ("All occurrences were cancelled — the whole booking "
                         "was removed.")
                    )
            else:
                # if no recurring booking -> permanent deletion of booking
                booking.delete()
                messages.success(request, "The single booking was deleted.")
        else:
            booking.delete()
            messages.success(
                request, "The entire series was deleted successfully.")

        # redirect to the same page
        # return redirect(request.path)

    return render(
        request,
        "appointments/booking_delete.html",
        {"booking": booking, "instance": instance}
    )


# --------------------------------------
# Send BookingInstance email invitation
# --------------------------------------

@login_required
def send_booking_invite_view(request, instance_id):
    # send email 
    instance = get_object_or_404(BookingInstance, id=instance_id)
    # Get the corresponding booking object
    booking = instance.booking

    if request.method == "POST":
        comment = request.POST.get("comment", "")
        attachment = request.FILES.get("attachment")
        recipients = [p.email for p in booking.participants.all()]

        # create ics file from instance data
        ics_file = generate_ics(booking, instance=instance)

        # Prepare email content
        subject = f"Invitation: {instance.current_title} on {
            instance.occurrence_date.strftime('%Y-%m-%d')}"
        body = (
            f"Hello,\n\n"
            f"You are invited to the following appointment:\n\n"
            f"Title: {instance.current_title}\n"
            f"Date: {instance.occurrence_date.strftime('%A, %d %B %Y')}\n"
            f"Start: {localtime(instance.current_start).strftime('%H:%M')}\n"
            f"End: {localtime(instance.current_end).strftime('%H:%M')}\n"
            f"{comment}\n\n"
            f"Regards,\n{request.user.get_full_name() or request.user.username}"
        )
        # send e-mail with attachment (ics(MIME)/other) if exists
        email = EmailMessage(subject, body, to=recipients)
        email.attach("invitation.ics", ics_file, "text/calendar")

        if attachment:
            email.attach(
                attachment.name, attachment.read(), attachment.content_type)

        email.send()

        messages.success(
            request, "E-mail with ics-file was sent successfully.")

    context = {
        "booking": booking,
        "instance": instance,
    }

    return render(request,
                  "appointments/send_invite.html", context)


# -----------------------------
# Booking PDF Export
# -----------------------------

@login_required
def booking_pdf(request):
    """Create a PDF from BookingInstance table with filters applied."""

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=landscape(A4), rightMargin=30, leftMargin=30,
        topMargin=30, bottomMargin=18)

    elements = []
    styles = getSampleStyleSheet()

    title_text = f"{request.user.first_name}'s Appointment overview"
    elements.append(Paragraph(title_text, styles["Title"]))
    elements.append(Spacer(1, 12))

    # all instances from current user
    instances = BookingInstance.objects.filter(
        Q(booking__booked_by=request.user) |
        Q(booking__participants=request.user),
        is_cancelled=False
    ).order_by("start").distinct()

    # Filter via BookingInstanceFilter (Day/Week/EventType)
    instance_filter = BookingInstanceFilter(request.GET, queryset=instances)
    filtered_instances = instance_filter.qs

    # prepare table
    data = [["Title", "Event Type", "Day", "Start",
             "End", "Status", "Participants"]]
    for inst in filtered_instances:
        booking = inst.booking
        participants = ", ".join(
            f"{p.first_name[0]}. {p.last_name}"
            if p.first_name and p.last_name else p.email
            for p in booking.participants.all()
        )
        # get local timzone
        start_local = localtime(inst.current_start)
        end_local = localtime(inst.current_end)

        data.append([
            inst.current_title,
            booking.event_type,
            start_local.strftime("%a"),
            start_local.strftime("%Y-%m-%d %H:%M"),
            end_local.strftime("%Y-%m-%d %H:%M"),
            booking.status,
            participants
        ])

    # style table
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


# -----------------------------
# Calendar View
# -----------------------------
class CalendarView(LoginRequiredMixin, generic.ListView):
    """Generate calendar for same team_members"""
    model = Booking
    template_name = "appointments/calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get("month"))
        context["prev_month"] = prev_month(d)
        context["next_month"] = next_month(d)

        first_day = d.replace(day=1)
        last_day = first_day + timedelta(
            days=calendar.monthrange(d.year, d.month)[1] - 1)

        # team of the logged_in user
        user_team = self.request.user.team_id

        # if user doesn't belong to a user_team, show empty calendar
        if not user_team:
            context["calendar"] = mark_safe(Calendar(
                d.year, d.month, events=[]
            ).formatmonth(withyear=True))
            return context

        # Filter: Only bookings of all team members, that are in the same team
        instances = BookingInstance.objects.filter(
            occurrence_date__gte=first_day,
            occurrence_date__lte=last_day,
            is_cancelled=False
        ).filter(
            Q(booking__booked_by__team_id=user_team) |
            Q(booking__participants__team_id=user_team)
        ).select_related('booking').distinct()

        # Generate calendar
        context["calendar"] = mark_safe(Calendar(
            d.year,
            d.month,
            events=[(inst.current_start, inst) for inst in instances]
        ).formatmonth(withyear=True))
        return context


def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split("-"))
        return date(year, month, 1)
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


# -----------------------------
# Day View
# -----------------------------
@login_required
def booking_day_view(request):
    current_user = request.user
    today = date.today()
    instances = BookingInstance.objects.filter(
        Q(booking__booked_by=current_user) |
        Q(booking__participants=current_user),
        occurrence_date=today,
        is_cancelled=False
    )
    context = {
        "bookings_today": instances.order_by("start"),
        "today": today
    }
    return render(request, "appointments/booking_day_view.html", context)
