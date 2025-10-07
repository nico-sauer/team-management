from django.forms import ModelForm
from django import forms

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
    last_updated =forms.DateField(widget=forms.SelectDateWidget)
    class Meta:
        model = AthleteProfile
        fields = [
            'height',
            'weight',
            'blood_type',
            'allergies',
            'prescriptions',
            'treatment_details',
            'diagnoses',
            'additional_notes',
            'last_updated'
            ]
        
