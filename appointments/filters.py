import django_filters
from appointments.models import BookingInstance
from django import forms
from datetime import timedelta


class BookingInstanceFilter(django_filters.FilterSet):
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
        return queryset.filter(occurrence_date__gte=value, occurrence_date__lt=week_end)

    class Meta:
        model = BookingInstance
        fields = ["booking__event_type"]
