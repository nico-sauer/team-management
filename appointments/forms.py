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

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start")
        end = cleaned_data.get("end")
                    
        now = timezone.now()

        # Start time needs to be in the future
        if start and start < timezone.now():
            self.add_error("start", "Start time must be in the future.")

        # End time needs to start after start time
        if start and end and end <= start:
            self.add_error("end", "End time must be after start time.")

        return cleaned_data
        
    
