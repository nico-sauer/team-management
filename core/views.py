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

            # If trainer, get athletes in their team.
            # NOTE: StaffProfile does not define a `team` field. The Team is
            # stored on the related `CustomUser` via the `team_id` ForeignKey.
            # Accessing `profile.team` will raise AttributeError, so we fetch
            # the team from the related user and filter athletes by the
            # user's `team_id`. If the trainer has no team (team_id is None)
            # we return an empty QuerySet instead of raising an error.
            if profile and getattr(profile, "role", None) == "Trainer":
                trainer_user = getattr(profile, "user", None)
                trainer_team = getattr(trainer_user, "team_id", None)
                if trainer_team:
                    athletes = AthleteProfile.objects.filter(user__team_id=trainer_team)
                else:
                    athletes = AthleteProfile.objects.none()

        context['profile'] = profile
        context['athletes'] = athletes
        return context