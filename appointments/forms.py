from django import forms
from .models import Booking
from django.utils import timezone
from django.core.exceptions import ValidationError


from django import forms
from .models import Booking

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
            "participants"
        ]
        widgets = {
            "start": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}),
            "end": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "event_type": forms.Select(attrs={"class": "form-select"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "participants": forms.SelectMultiple(attrs={"class": "form-select"}),
        }
    
    """
    Check, if participants are selected before saving the form.
    """
    def clean_participants(self):
        participants = self.cleaned_data.get("participants")
        if not participants:
            raise forms.ValidationError("Please select at least one participant.")
        return participants
        
    """
    Validation for start and end times to ensure they are in the future and valid dates.
    """
    def clean_start(self):
        start = self.cleaned_data.get("start")
        if start < timezone.now():
            raise ValidationError("Start time must be in the future.")
        return start
    
    def clean_end(self):
        end = self.cleaned_data.get("end")
        if end <= self.cleaned_data.get("start"):
            raise ValidationError("End time must be after start time.")
        return end