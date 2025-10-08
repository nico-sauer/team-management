from django.db import models
from users.models import CustomUser
from datetime import timedelta, date
# from django.utils.timezone import make_aware, get_current_timezone, is_aware
import calendar

""" 
Team members can create a booking if all participants
they request to have this timeslot not already booked.
"""


class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("rejected", "Rejected"),
    ]

    EVENT_TYPES = [
        ("meeting", "Meeting"),
        ("training", "Training"),
        ("match", "Match"),
        ("physio", "Physio"),
        ("private", "Private"),
        ("other", "Other"),
    ]

    RECURRENCES = [
        ("none", "Once"),
        ("daily", "Daily"),
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
    ]

    title = models.CharField(max_length=100, blank=True)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES,
                                  default="meeting")
    booked_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="bookings_by"
    )
    start = models.DateTimeField()
    end = models.DateTimeField()
    location = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
                              default="pending")
    created_at = models.DateTimeField(auto_now_add=True, null=False)

    participants = models.ManyToManyField(
        CustomUser, blank=True, related_name="participating_bookings")

    recurrence = models.CharField(
        max_length=20, choices=RECURRENCES, default="none")
    recurrence_end = models.DateField(null=True, blank=True, 
                                      help_text="Repetition until when?")

    def __str__(self):
        return (
            self.title
            or f"{self.event_type} ({self.start} - {self.end}) @ {self.location}"
        )

    """ checks, if a participant has another booking at the same time.
    If yes, return a list with 'conflicting' participants. """
    def is_conflicting(self, participants=None):
        # check if participants are given as argument
        if participants is None:
            raise ValueError("Participants must not be empty.")

        conflicts = []
        for participant in participants:
            overlapping = Booking.objects.filter(
                participants=participant,
                start__lt=self.end,
                end__gt=self.start,
                status__in=["pending", "confirmed"],
            ).exclude(id=self.id)
            if overlapping.exists():
                conflicts.append(participant)
        return conflicts

    def get_occurrences(self, from_date=None, to_date=None):
        """
        Returns a list of all occurrences of this booking in
        the given date range. All datetimes are timezone-aware.
        """
        if from_date is None or to_date is None:
            raise ValueError("from_date and to_date must be provided")

        occurrences = []

        occurance_date = self.start.date()
        recurrence_end = self.recurrence_end or self.start.date()

        if self.recurrence == "none":
            if from_date <= occurance_date <= to_date:
                occurrences.append(self.start)
            return occurrences

        delta = {
            "daily": timedelta(days=1),
            "weekly": timedelta(weeks=1),
            "monthly": None,    # special case, as diff amount of days exists
        }.get(self.recurrence)

        while occurance_date <= recurrence_end:
            if from_date <= occurance_date <= to_date:
                dt = self.start.replace(year=occurance_date.year,
                                        month=occurance_date.month,
                                        day=occurance_date.day)
                occurrences.append(dt)

            # calculate next monthly date
            if self.recurrence == "monthly":
                next_month = (occurance_date.month % 12) + 1
                year = occurance_date.year + (occurance_date.month // 12)
                last_day_of_month = calendar.monthrange(year, next_month)[1]
                day = min(occurance_date.day, last_day_of_month)
                occurance_date = date(year, next_month, day)
            else:
                occurance_date += delta
        return occurrences
