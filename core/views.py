from django.shortcuts import render
from django.views.generic import TemplateView 
from profiles.models import StaffProfile, AthleteProfile 

class HomePageView(TemplateView): 
    template_name = 'home.html' 
    
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 
        user = self.request.user
        profile = None
        athletes = []

        if user.is_authenticated:
            # Check for staff profile first
            try:
                profile = StaffProfile.objects.get(user=user)
            except StaffProfile.DoesNotExist:
                # If not staff, check for athlete profile
                try:
                    profile = AthleteProfile.objects.get(user=user)
                except AthleteProfile.DoesNotExist:
                    profile = None

            # If trainer, get athletes in their team
            if profile and getattr(profile, "role", None) == "Trainer":
                athletes = AthleteProfile.objects.filter(team=profile.team)

        context['profile'] = profile
        context['athletes'] = athletes
        return context