from django import forms
from .models import Booking
from users.models import CustomUser
from django.utils import timezone
from datetime import datetime, time


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            "title",
            "event_type",
            "start",
            "end",
            "location",
            "status",
            "participants",
            "recurrence",
            "recurrence_end",
        ]
        widgets = {
            "start": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"}
            ),
            "end": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"}
            ),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "event_type": forms.Select(attrs={"class": "form-select"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "participants": forms.SelectMultiple(attrs={"class": "form-select"}),
            "recurrence_end": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
        }
        labels = {
            "recurrence_end": "Recurrence end date:",
        }

    def __init__(self, *args, **kwargs):
        # current_user is passed when the form is initialized
        self.current_user = kwargs.pop("current_user", None)
        super().__init__(*args, **kwargs)
        self.fields["participants"].label_from_instance = lambda u: (
            f"{u.first_name[0]}. {u.last_name}"
            if u.first_name and u.last_name
            else u.email
        )
        if self.current_user:
            # Filter only user from the current user team_id
            self.fields["participants"].queryset = CustomUser.objects.filter(
                team_id=self.current_user.team_id
            )

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start")
        end = cleaned_data.get("end")
        recurrence_end = cleaned_data.get("recurrence_end")
        participants = cleaned_data.get("participants")

        now = timezone.now()

        # time-validations
        if start and start < now:
            self.add_error("start", "Start time must be in the future.")

        if start and end and end <= start:
            self.add_error("end", "End time must be after start time.")

        # assure recurrence_end is in datetime format
        if recurrence_end and isinstance(recurrence_end, datetime) is False:
            recurrence_end = datetime.combine(recurrence_end, time.min)

        # assure that all times are timezone aware
        if recurrence_end and timezone.is_naive(recurrence_end):
            recurrence_end = timezone.make_aware(
                recurrence_end, timezone.get_current_timezone()
            )

        # get sure recurrence_end is after start-date
        if start and recurrence_end:
            if recurrence_end <= start:
                self.add_error(
                    "recurrence_end",
                    "Recurrence end date must be after the start date.",
                )
        # participants-validations, team-check & min-amount of participants
        if not participants:
            self.add_error("participants", "Please select at least one participant.")
        elif self.current_user:
            for p in participants:
                if p.team_id != self.current_user.team_id:
                    self.add_error(
                        "participants",
                        f"{p} is not in the same team as {self.current_user}",
                    )

        return cleaned_data
