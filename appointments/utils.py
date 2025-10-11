#  from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Booking
from datetime import date, timedelta
from django.utils.timezone import localtime


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None, events=None):
        self.year = year
        self.month = month
        self.events = events or []  
        super(Calendar, self).__init__()

    def get_month_date_range(self):
        """Get first and last day of the month."""
        first_day = date(self.year, self.month, 1)
        if self.month == 12:
            next_month = date(self.year + 1, 1, 1)
        else:
            next_month = date(self.year, self.month + 1, 1)
        last_day = next_month - timedelta(days=1)
        return first_day, last_day

    def formatday(self, day, bookings):
        if day == 0:
            return "<td></td>"

        current_date = date(self.year, self.month, day)
        d = ""

        # only one-time_bookings
        one_time_bookings = bookings.filter(
            recurrence="none", start__date=current_date)

        # recurring bookings
        recurring_bookings = []
        for booking in bookings.exclude(recurrence="none"):
            occurrences = booking.get_occurrences(current_date, current_date)
            if occurrences:
                recurring_bookings.append(booking)

        # all bookings without duplicates one-time & recurring bookings
        all_bookings = list(
            {b.id: b for b in list(one_time_bookings)
             + recurring_bookings}.values())

        # sort chronologically by start_time
        all_bookings.sort(key=lambda b: b.start)

        css_class = (
            # "private"
            # "has-private" if any(b.event_type == "private" for b in
            #                      all_bookings) else ""
        )
        # optional 
        day_url = f"/appointments/day_view/?date={self.year}-{self.month:02d}-{day:02d}"
        
        for booking in all_bookings:
            local_start = localtime(booking.start)
            local_end = localtime(booking.end)
            time_str = f"{
                local_start.strftime('%H:%M')}-{local_end.strftime('%H:%M')}"
            
            if booking.booked_by.first_name and booking.booked_by.last_name:
                username = (f"{booking.booked_by.first_name[0]}."
                            f" {booking.booked_by.last_name}")
            else:
                username = str(booking.booked_by)
             
            if booking.status == "pending":
                d += f"<li class='pending'>{time_str} Event pending</li>"
            elif booking.event_type == "private":
                d += f"<li class='private'>{time_str} Private<br>{username}</li>"
            elif booking.event_type == "training":
                d += f"<li class='training'>{time_str} {booking.title}</li>"
            else:
                d += f"<li class='other'>{time_str} {booking.title}</li>"

        return f"<td class='{css_class}'><span class='date'>{day}</span><ul>{d}</ul></td>"

    # formats a week as a <tr>
    def formatweek(self, theweek, bookings):
        week = ""
        for d, weekday in theweek:
            week += self.formatday(d, bookings)
        return f"<tr> {week} </tr>"

    # formats a month as a complete table
    def formatmonth(self, withyear=True):
        first_day, last_day = self.get_month_date_range()

        # only bookings, which are in this month range
        events = Booking.objects.filter(
            start__lte=last_day,
            end__gte=first_day,
        )

        cal = '<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f"{self.formatmonthname(
            self.year, self.month, withyear=withyear)}\n"
        cal += f"{self.formatweekheader()}\n"
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f"{self.formatweek(week, events)}\n"
        cal += "</table>"
        return cal
