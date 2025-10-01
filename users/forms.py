from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Team, CustomUser
from django.contrib.auth.models import Group


# User = get_user_model()


ROLE_CHOICES =(
    
    ("Manager", "Manager"),
    ("Trainer", "Trainer"),
    ("Physical Therapist", "Physical Therapist"),
    ("Dietitian", "Dietician"),
    ("Doctor", "Doctor"),
    ("Athlete", "Athlete"),
)

class CustomUserCreationForm(UserCreationForm, forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    
    role= forms.ChoiceField(choices=ROLE_CHOICES)
    team_id = forms.ModelChoiceField(queryset=Team.objects.all())
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
            'team_id',
            'group',
        ]
        
    # to test the group editor
        
    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.set_password(self.cleaned_data["password"])
    #     if commit:
    #         user.save()
    #         group = self.cleaed_data['group'] 
    #         user.groups.set([group])
            
    #     return user
    


