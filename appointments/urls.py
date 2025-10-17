from django.urls import path
from . import views

app_name = "appointments"

urlpatterns = [
    path("booking_create/", views.create_booking, name="booking"),
    path("bookings/", views.booking_list, name="booking_list"),
    path("booking/<int:booking_id>/instance/<int:instance_id>/edit/",
         views.edit_booking_instance, name="booking_instance_edit",),
    path("bookings/<int:pk>/delete", views.delete_booking,
         name="delete_booking"),
    path("booking/<int:pk>/instance/<int:instance_id>/delete/",
         views.delete_booking, name="delete_booking_instance"),
    path("calendar/", views.CalendarView.as_view(), name="calendar"),
    path("booking_pdf/", views.booking_pdf, name="booking_pdf"),
    path("booking_day_view/", views.booking_day_view, name="booking_day_view"),
    path('booking/<int:booking_id>/send_invite/',
         views.send_booking_invite_view, name='send_invite'),
]
