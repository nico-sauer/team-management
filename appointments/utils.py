#  from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Booking
from datetime import date, timedelta
from django.utils.timezone import localtime
from django.utils.timezone import make_aware, get_current_timezone, is_aware


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

    def formatday(self, day, weekday, bookings):
        if day == 0:
            return "<td></td>"

        current_date = date(self.year, self.month, day)
        d = ""

        # only one-time_bookings
        one_time_bookings = bookings.filter(recurrence="none", start__date=current_date)

        # recurring bookings
        recurring_bookings = []
        for booking in bookings.exclude(recurrence="none"):
            occurrences = booking.get_occurrences(current_date, current_date)
            if occurrences:
                recurring_bookings.append(booking)

        # all bookings without duplicates one-time & recurring bookings
        all_bookings = list(
            {b.id: b for b in list(one_time_bookings) + recurring_bookings}.values()
        )

        # sort chronologically by start_time
        all_bookings.sort(key=lambda b: b.start)

        css_class = ""

        for booking in all_bookings:
            local_start = localtime(booking.start)
            local_end = localtime(booking.end)
            time_str = (
                f"{local_start.strftime('%H:%M')}-" f"{local_end.strftime('%H:%M')}"
            )

            if booking.booked_by.first_name and booking.booked_by.last_name:
                username = (
                    f"{booking.booked_by.first_name[0]}."
                    f" {booking.booked_by.last_name}"
                )
            else:
                username = str(booking.booked_by)

            if booking.status == "rejected":
                d += (
                    f"<li class='rejected'>{time_str} {booking.title}" f"rejected </li>"
                )
            elif booking.event_type == "private":
                d += f"<li class='private'>{time_str} " f"Private<br>{username}</li>"
            elif booking.event_type == "training":
                d += f"<li class='training'>{time_str} {booking.title}</li>"

            else:
                d += f"<li class='other'>{time_str} {booking.title}</li>"

        return (
            f"<td class='{css_class}'><span class='date'>{day}</span><ul>{d}"
            f"</ul></td>"
        )

    # formats a week as a <tr>
    def formatweek(self, theweek, bookings):
        week = ""
        for d, weekday in theweek:
            week += self.formatday(d, weekday, bookings)
        return f"<tr> {week} </tr>"

    # formats a month as a complete table
    def formatmonth(self, withyear=True):
        first_day, last_day = self.get_month_date_range()

        # only bookings, which are in this month range
        events = Booking.objects.filter(
            start__lte=last_day,
            end__gte=first_day,
        )

        cal = '<table border="0" cellpadding="0" cellspacing="0"' 'class="calendar">\n'
        cal += f"{self.formatmonthname(
            self.year, self.month, withyear=withyear)}\n"
        cal += f"{self.formatweekheader()}\n"
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f"{self.formatweek(week, events)}\n"
        cal += "</table>"
        return cal


# get expanded bookings for booking_list & booking_list_pdf
def expand_bookings(filtered_bookings, start_date, end_date):
    """Expand recurring and non-recurring bookings
    into individual occurrences."""
    tz = get_current_timezone()
    expanded = []

    for booking in filtered_bookings:
        if booking.recurrence != "none":
            occurrences = booking.get_occurrences(start_date, end_date)
            for occ_start in occurrences:
                duration = booking.end - booking.start
                occ_end = occ_start + duration

                if not is_aware(occ_start):
                    occ_start = make_aware(occ_start, tz)
                if not is_aware(occ_end):
                    occ_end = make_aware(occ_end, tz)

                expanded.append(
                    {
                        "booking": booking,
                        "occurrence": occ_start,
                        "end_occurrence": occ_end,
                    }
                )
        else:
            start = booking.start
            end = booking.end
            if not is_aware(start):
                start = make_aware(start, tz)
            if not is_aware(end):
                end = make_aware(end, tz)

            expanded.append(
                {
                    "booking": booking,
                    "occurrence": start,
                    "end_occurrence": end,
                }
            )

    # Sort by occurrence start
    expanded.sort(key=lambda x: x["occurrence"])
    return expanded
