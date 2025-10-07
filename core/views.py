from django.shortcuts import render
from django.views.generic import TemplateView 
from profiles.models import StaffProfile, AthleteProfile 

class HomePageView(TemplateView): 
    template_name = 'home.html' 
    
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 
        profile = None
        user = self.request.user
        if user.is_authenticated:
            try:
                profile = StaffProfile.objects.get(user=user)
            except StaffProfile.DoesNotExist:
                try:
                    profile = AthleteProfile.objects.get(user=user)
                except AthleteProfile.DoesNotExist:
                    profile = None
        context['profile'] = profile        
        return context