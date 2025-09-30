from django import forms
from .models import Booking
from users.models import CustomUser
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
    
    def __init__(self, *args, **kwargs):
        # current_user is passed when the form is initialized 
        self.current_user = kwargs.pop("current_user", None)
        super().__init__(*args, **kwargs)
        if self.current_user:
            # Filter only user from the current user team_id
            self.fields["participants"].queryset = CustomUser.objects.filter(team_id=self.current_user.team_id)
            
    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start")
        end = cleaned_data.get("end")
        participants = cleaned_data.get("participants")
        
        now = timezone.now()

        # time-validations
        if start and start < now:
            self.add_error("start", "Start time must be in the future.")

        if start and end and end <= start:
            self.add_error("end", "End time must be after start time.")

        # participants-validations, a minimum of on existing teammember needs to be choosen
        if not participants:
            self.add_error("participants", "Please select at least one participant.")
        elif self.current_user:
            for p in participants:
                if p.team_id != self.current_user.team_id:
                    self.add_error(
                        "participants",
                        f"{p} is not in the same team as {self.current_user}"
                    )

        return cleaned_data    
        
        
        
    
   
    
