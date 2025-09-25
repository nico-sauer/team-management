from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .forms import BookingForm
from datetime import datetime
from datetime import datetime, timedelta, date

from django.views import generic
from django.utils.safestring import mark_safe
from .utils import Calendar
import calendar  # python standard calendar


def create_booking(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            # Don't save the booking before checking for conflicts
            booking = form.save(commit=False)
            booking.booked_by = request.user
            
            # get all selected participants from form
            participants = form.cleaned_data["participants"]
            
            # checks, if participants are already booked at that time
            conflicts = booking.is_conflicting(participants=participants)
            if conflicts:
                conflicts_names = ", ".join([str(participant) for participant in conflicts])
                messages.error(request,
                    f"Find another timeslot, as {conflicts_names} is/are already booked.")
                # form not valid so render the form again
                return render(request, "appointments/booking_create.html", {"form": form})

            # if form is valid and no conflict found -> save booking, than save m2m relations and show success message
            booking.save()
            form.save_m2m()  # save ManyToMany relation after the database has been saved
            
            messages.success(request, "Booking was succesfull")
            return redirect("appointments:booking_list")
    else:
        form = BookingForm()
    return render(request, "appointments/booking_create.html", {"form": form})



def booking_list(request):
    bookings = Booking.objects.all().order_by("-created_at") # latest bookings first (-)
    return render(request, "appointments/booking_list.html", {"bookings": bookings})


def edit_booking(request, pk):
    booking = Booking.objects.get(pk=pk)
    if request.method == "POST":
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect("appointments:booking_list")
    else:
        form = BookingForm(instance=booking)
    return render(request, "appointments/booking_edit.html", {"form": form})

def delete_booking(request, pk):
    booking = Booking.objects.get(pk=pk)
    if request.method == "POST":
        booking.delete()
        return redirect("appointments:booking_list")
    return render(request, "appointments/booking_delete.html", {"booking": booking})

#----------------
# calendar

class CalendarView(generic.ListView):
    model = Booking
    template_name = 'appointments/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date/month for the calendar
        d = get_date(self.request.GET.get('month', None))
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
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


