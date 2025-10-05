import django_filters
from appointments.models import Booking
from django import forms


class BookingFilter(django_filters.FilterSet):
    start = django_filters.DateFilter(
        lookup_expr="gte",
        widget=forms.TextInput(
            attrs={
                "placeholder": "YYYY-MM-DD",
                "class": "form-control",
            }
        ),
        label="Start date (from)",
        )
    
    
    

    class Meta:
        model = Booking
        fields = ["event_type", "status", "start"]
