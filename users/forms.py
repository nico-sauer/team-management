from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Team, CustomUser



# User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    
    
    class Meta:
        model = CustomUser
        fields = [

            'first_name',
            'last_name', 
            'email',
            'password1',
            'password2',
        ]
    #def save(self, commit=True):
     #   user = super().save(commit=False)
      #  user.set_password(self.cleaned_data["password"])
       # if commit:
        #    user.save()
            
        #return user
    


