from django.urls import path
from . import views

app_name = "appointments"

urlpatterns = [
    path("booking_create/", views.create_booking, name="booking"),
    path("bookings/", views.booking_list, name="booking_list"),
    path("bookings/<int:pk>/edit", views.edit_booking, name="edit_booking"),
    path("bookings/<int:pk>/delete", views.delete_booking,
         name="delete_booking"),
    path("calendar/", views.CalendarView.as_view(), name="calendar"),
    path("booking_pdf/", views.booking_pdf, name="booking_pdf"),
]
