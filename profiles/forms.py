from django.forms import ModelForm

from .models import StaffProfile


class StaffRoles(ModelForm):
    class Meta:
        model = StaffProfile
        fields = ['role']
        
class StaffTitle(ModelForm):
    class Meta:
        model = StaffProfile
        fields = ['title']