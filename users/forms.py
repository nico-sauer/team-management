from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Team, CustomUser
from django.contrib.auth.models import Group

ROLE_CHOICES =(
    
    ("Manager", "Manager"),
    ("Trainer", "Trainer"),
    ("Physical Therapist", "Physical Therapist"),
    ("Dietitian", "Dietitian"),
    ("Doctor", "Doctor"),
    ("Athlete", "Athlete"),
)

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    
    role= forms.ChoiceField(choices=ROLE_CHOICES)
    
    team = forms.ModelChoiceField(queryset=Team.objects.all(), required=False)
    
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=False)
    new_group_name = forms.CharField(required=False, label="Create new group")
    
    new_team_name = forms.CharField(required=False, label="Create new team")
   
    class Meta:
        model = CustomUser
        fields = [

            'first_name',
            'last_name', 
            'email',
            'password1',
            'password2',
            
            'role',
            # 'team',
            'group',
        ]
    
        
    def save(self, commit=True):
        user = super().save(commit=False)
        new_team_name = self.cleaned_data.get('new_team_name')
        new_group_name = self.cleaned_data.get('new_group_name')

        # team
        if new_team_name:
            team = Team.objects.create(team_name=new_team_name)
            user.team = team
        elif self.cleaned_data.get('team'):
            user.team = self.cleaned_data['team']

        # group
        if new_group_name:
            group = Group.objects.create(name=new_group_name)
        elif self.cleaned_data.get('group'):
            group = self.cleaned_data['group']
        else:
            group = None

        if commit:
            user.save()
            if group:
                user.groups.add(group)
        return user
    

#A form for the first team member that register(Manager)
class FirstCustomUserCreationForm(UserCreationForm, forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    
    role= forms.ChoiceField(choices=ROLE_CHOICES, initial='Manager', required=False)
    team = forms.ModelChoiceField(queryset=Team.objects.all(), required=False)
    
    group = forms.ModelChoiceField(queryset=Group.objects.all(), initial= 'Managers', required=False),
    
    class Meta:
        model = CustomUser
        fields = [

            'first_name',
            'last_name', 
            'email',
            'password1',
            'password2',
            
            # 'role',
            'team',
            # 'group',
        ]
    
        
    def save(self, commit=True):
        user = super().save(commit=False)
        
        # group = self.cleaned_data['group']
        group= Group.objects.get(name='Managers') 
        
        team = self.cleaned_data['team']
        team = Team.objects.create(team_name = team, manager = 'first_name') #can be change to get_or_create if we want the manager to use an existing team
        user.team=team
        
        if commit:
            role = 'Manager'
            user.role = role
            user.groups.add(group)
            user.save()
            
            
        # user.groups.set([group]) if we want more then one group to one user
            
        return user