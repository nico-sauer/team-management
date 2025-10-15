from django.contrib import admin
from .models import Booking

# Register your models here.


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "event_type",
        "status",
        "booked_by",
        "location",
        "recurrence",
    ]
