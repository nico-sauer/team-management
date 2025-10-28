from calendar import HTMLCalendar
from .models import BookingInstance
from datetime import date, timedelta
from django.utils.timezone import localtime
# from django.utils.timezone import make_aware, get_current_timezone, is_aware


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

        # all BookingInstances for the current day
        day_instances = [
            inst for inst in bookings if inst.occurrence_date == current_date]

        # sort chronologically by start_time
        day_instances.sort(key=lambda inst: inst.current_start)

        css_class = ""

        for inst in day_instances:
            booking = inst.booking
            local_start = localtime(inst.current_start)
            local_end = localtime(inst.current_end)
            time_str = f"{local_start.strftime('%H:%M')}-{local_end.strftime('%H:%M')}"
            username = (
                f"{inst.booking.booked_by.first_name[0]}. {
                    inst.booking.booked_by.last_name}"
                if inst.booking.booked_by.first_name
                and inst.booking.booked_by.last_name
                else str(inst.booking.booked_by)
            )

            if booking.status == "rejected":
                d += (f"<li class='rejected'>{time_str} "
                      f"{inst.current_title} rejected</li>")
            elif booking.event_type == "private":
                d += (f"<li class='private'>{time_str}"
                      f" Private <br>{username}</li>")
            elif booking.event_type == "training":
                d += f"<li class='training'>{time_str} {
                    inst.current_title}</li>"
            else:
                d += f"<li class='other'>{time_str} {
                    inst.current_title}</li>"

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

        instances = [inst for _, inst in self.events
                     if first_day <= inst.occurrence_date <= last_day]

        cal = (
            '<table border="0" cellpadding="0" cellspacing="0"''class="calendar">\n')
        cal += f"{self.formatmonthname(
            self.year, self.month, withyear=withyear)}\n"
        cal += f"{self.formatweekheader()}\n"
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f"{self.formatweek(week, instances)}\n"
        cal += "</table>"
        return cal

