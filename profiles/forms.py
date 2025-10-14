from django import forms
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit

from .models import AthleteProfile, StaffProfile


class StaffRoles(ModelForm):
    class Meta:
        model = StaffProfile
        fields = ['role']
        
class StaffTitle(ModelForm):
    class Meta:
        model = StaffProfile
        fields = ['title']
        


class BloodType(ModelForm):
    class Meta:
        model = AthleteProfile
        fields = ['blood_type']
        
class Gender(ModelForm):
    class Meta:
        model = AthleteProfile
        fields = ['gender']
        
        
class AthleteProfileForm(ModelForm):
    #allergies = forms.TextInput() 
    #last_updated =forms.DateField(widget=forms.SelectDateWidget)
    class Meta:
        model = AthleteProfile
        fields = '__all__'
        
class StaffProfileForm(ModelForm):
    
    class Meta:
        model = StaffProfile
        fields = "__all__"