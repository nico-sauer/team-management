from django.db import models
from users.models import CustomUser
from django.core.exceptions import ValidationError

''' 
Team members can create a booking if all participants
they request to have this timeslot not already booked.
'''
class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("rejected", "Rejected"),
    ]
    
    Event_Types = [
        ('meeting', 'Meeting'),
        ('training', 'Training'),
        ('match', 'Match'),
        ('physio', 'Physio'),
        ('private', 'Private'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=100, blank=True) 
    event_type = models.CharField(max_length=50, choices=Event_Types, default='meeting')
    booked_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="bookings_by")
    start = models.DateTimeField()
    end = models.DateTimeField()
    location = models.CharField(max_length=100, blank=True) 
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    
    participants = models.ManyToManyField(CustomUser, blank=True, related_name="participating_bookings")    

    def __str__(self):
        return self.title or f"{self.event_type} ({self.start} - {self.end}) @ {self.location}"
    
    
    """ checks, if a participant has another booking at the same time.
    If yes, return a list with 'conflicting' participants. """
    def is_conflicting(self, participants=None):
        # check if participants are given as argument
        if participants is None:
            raise ValueError("Participants must not be empty.")
        
        conflicts = []
        for participant in participants:
            overlapping = Booking.objects.filter(
                participants=participant,
                start__lt=self.end,
                end__gt=self.start,
                status__in=["pending", "confirmed"]
            ).exclude(id=self.id)
            if overlapping.exists():
                conflicts.append(participant)
        return conflicts
    
    
   