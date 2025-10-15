import django_filters
from appointments.models import Booking
from django import forms


class BookingFilter(django_filters.FilterSet):
    # day_view = django_filters.DateFilter(
    #     field_name="start",
    #     lookup_expr="date",
    #     widget=forms.TextInput(
    #         attrs={
    #             "placeholder": "YYYY-MM-DD",
    #             "class": "form-control",
    #         }
    #     ),
    #     label="Day view",
    #     )

    # start_from = django_filters.DateFilter(
    #     field_name="start",
    #     lookup_expr="gte",
    #     widget=forms.TextInput(
    #         attrs={
    #             "placeholder": "YYYY-MM-DD",
    #             "class": "form-control",
    #         }
    #     ),
    #     label="Start date (from)",
    #     )

    class Meta:
        model = Booking
        fields = ["event_type"]
