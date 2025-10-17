from django.db import models
from users.models import CustomUser
from datetime import timedelta, date

import calendar


class Booking(models.Model):
    STATUS_CHOICES = [
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
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES, default="meeting")
    booked_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="bookings_by"
    )
    start = models.DateTimeField()
    end = models.DateTimeField()
    location = models.CharField(max_length=100, blank=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="confirmed"
    )
    created_at = models.DateTimeField(auto_now_add=True, null=False)

    participants = models.ManyToManyField(
        CustomUser, blank=True, related_name="participating_bookings"
    )

    recurrence = models.CharField(
        max_length=20,
        choices=RECURRENCES,
        default="none",
        help_text=(
            "Select daily, weekly or monthly for repeating events, "
            "or ignore rubric recurrence/end."
        ),
    )
    recurrence_end = models.DateField(
        null=True, blank=True, help_text="Repetition until when?"
    )

    def __str__(self):
        return (
            self.title
            or f"{self.event_type} ({self.start} - {self.end}) @ {self.location}"
        )

    def is_conflicting(self, participants=None, instance=None):
        """
        Checks if a participant has another booking at the same time.
        If 'instance' is provided, consider its modified start/end times.
        Returns a list of conflicting participants.
        """

        if participants is None:
            raise ValueError("Participants must not be empty.")

        conflicts = []

        # use instance times if editing a single BookingInstance
        start_time = instance.current_start if instance else self.start
        end_time = instance.current_end if instance else self.end

        from_date = (start_time.date() - timedelta(days=1))
        to_date = (end_time.date() + timedelta(days=1))

        for participant in participants:
            # get all relevant bookings
            bookings = Booking.objects.filter(
                participants=participant, status__in=["confirmed"]
            ).exclude(id=self.id)

            # include BookingInstances (for modified instances)
            instances = BookingInstance.objects.filter(
                booking__participants=participant,
                is_cancelled=False,
            )
            if instance:
                instances = instances.exclude(id=instance.id)

            # check conflicts in bookings
            for other in bookings:
                if other.recurrence == "none":
                    if other.start < end_time and other.end > start_time:
                        conflicts.append(participant)
                        break
                else:
                    occurrences = other.get_occurrences(from_date, to_date)
                    for occ_start in occurrences:
                        occ_end = occ_start + (other.end - other.start)
                        if occ_start < end_time and occ_end > start_time:
                            conflicts.append(participant)
                            break

            # check conflicts in BookingInstances
            for inst in instances:
                inst_start = inst.current_start
                inst_end = inst.current_end
                if inst_start < end_time and inst_end > start_time:
                    conflicts.append(participant)
                    break

        return list(set(conflicts))

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
            "monthly": None,  # special case, as diff amount of days exists
        }.get(self.recurrence)

        while occurance_date <= recurrence_end:
            if from_date <= occurance_date <= to_date:
                dt = self.start.replace(
                    year=occurance_date.year,
                    month=occurance_date.month,
                    day=occurance_date.day,
                )
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
        return occurrences  # [datetime(2025,10,01,10,0)/2025-10-01 09:00:00]

    def generate_booking_instances(self):
        """Create database entries for BookingInstance
           from Booking model and get_occurences()"""
        if self.recurrence == "none":
            # get/or create on-time booking, if not already exist
            BookingInstance.objects.get_or_create(
                booking=self,
                occurrence_date=self.start.date(),
                defaults={
                    "start": self.start,
                    "end": self.end,
                },
            )
            return

        from_date = self.start.date()
        to_date = self.recurrence_end or from_date
        occurrences = self.get_occurrences(from_date, to_date)

        for occ_start in occurrences:
            BookingInstance.objects.get_or_create(
                booking=self,
                occurrence_date=occ_start.date(),
                defaults={
                    "start": occ_start,
                    "end": occ_start + (self.end - self.start),
                },
            )


class BookingInstance(models.Model):
    """creating a table with all booking instances, to have
       the chance to delete and change single events (incl. recurring)
       from one database table. Before recurring events didn't exist in a DB"""
    booking = models.ForeignKey(
        'Booking',
        on_delete=models.CASCADE,
        related_name='all_booking_instances'
    )
    occurrence_date = models.DateField()
    start = models.DateTimeField()
    end = models.DateTimeField()

    # track booking_changes
    is_cancelled = models.BooleanField(default=False)
    is_modified = models.BooleanField(default=False)

    # track title, start- or end time changes
    override_title = models.CharField(null=True, blank=True)
    override_start = models.DateTimeField(null=True, blank=True)
    override_end = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('booking', 'occurrence_date')
        ordering = ['start']

    def __str__(self):
        return f"{self.booking.title} ({self.occurrence_date})"

    @property
    def current_title(self):
        return self.override_title or self.booking.title

    @property
    def current_start(self):
        return self.override_start or self.start

    @property
    def current_end(self):
        return self.override_end or self.end
