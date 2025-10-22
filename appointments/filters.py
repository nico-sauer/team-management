import django_filters
from appointments.models import BookingInstance, Booking
from django import forms
from datetime import timedelta


class BookingInstanceFilter(django_filters.FilterSet):

    booking_event_type = django_filters.ChoiceFilter(
        field_name="booking__event_type",
        choices=Booking.EVENT_TYPES,
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ),
        label="Event type",
    )

    booking_status = django_filters.ChoiceFilter(
        field_name="booking__status",
        choices=Booking.STATUS_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ),
        label="Event status",
    )

    day_view = django_filters.DateFilter(
        field_name="occurrence_date",
        lookup_expr="exact",
        widget=forms.TextInput(
            attrs={
                "placeholder": "YYYY-MM-DD",
                "class": "form-control",
            }
        ),
        label="Day view",
    )

    week_view = django_filters.DateFilter(
        field_name="occurrence_date",
        lookup_expr="gte",
        widget=forms.TextInput(
            attrs={
                "placeholder": "YYYY-MM-DD",
                "class": "form-control",
            }
        ),
        label="Week view from",
    )

    def filter_week(self, queryset, name, value):
        week_end = value + timedelta(days=7)
        return queryset.filter(
            occurrence_date__gte=value, occurrence_date__lt=week_end)

    class Meta:
        model = BookingInstance
        fields = []
