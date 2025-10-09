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
            # Try all profile types
            for ProfileModel in [StaffProfile, AthleteProfile]:
                try:
                    profile = ProfileModel.objects.get(user=user)
                    break
                except ProfileModel.DoesNotExist:
                    continue
        context['profile'] = profile        
        return context