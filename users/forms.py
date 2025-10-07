from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Team, CustomUser
from django.contrib.auth.models import Group

ROLE_CHOICES =(
    
    # ("Manager", "Manager"),
    ("Trainer", "Trainer"),
    ("Physical Therapist", "Physical Therapist"),
    ("Dietitian", "Dietitian"),
    ("Doctor", "Doctor"),
    ("Athlete", "Athlete"),
)

class CustomUserCreationForm(UserCreationForm, forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    
    role= forms.ChoiceField(choices=ROLE_CHOICES)
    team = forms.ModelChoiceField(queryset=Team.objects.all())
    group = forms.ModelChoiceField(queryset=Group.objects.all())
    
   
    class Meta:
        model = CustomUser
        fields = [

            'first_name',
            'last_name', 
            'email',
            'password1',
            'password2',
            
            'role',
            'team',
            'group',
        ]
    
        
    def save(self, commit=True):
        user = super().save(commit=False)
        group = self.cleaned_data['group']
        
        manager_user_id = current_user.id give the id of the logged in user
    # manager_team= staffprofile.objects.get(pk=user_id).filter(team_id)
        if user.team != team
        
        if commit:
            user.save()
            user.groups.add(group)
        # user.groups.set([group]) if we want more then one group to one user
            
        return user
    


class FirstCustomUserCreationForm(UserCreationForm, forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    
    role= forms.ChoiceField(choices=ROLE_CHOICES, default='Manager', null=True, blank=True)
    team = forms.CharField(max_length=250)
    
    # team = forms.ModelChoiceField(queryset=Team.objects.all())
    group = forms.ModelChoiceField(queryset=Group.objects.all(), default = 'Managers', null=True, blank=True),
    
    class Meta:
        model = CustomUser
        fields = [

            'first_name',
            'last_name', 
            'email',
            'password1',
            'password2',
            
            'role',
            'team',
            'group',
        ]
    
        
    def save(self, commit=True):
        user = super().save(commit=False)
        
        group = self.cleaned_data['group']
        
        team = self.cleaned_data['team']
        team = Team.objects.create(name = team, manager = 'first_name') #can be change to get_or_create if we want the manager to use an existing team
        user.team=team
        
        if commit:
            user.save()
            user.groups.add(group)
            
        # user.groups.set([group]) if we want more then one group to one user
            
        return user