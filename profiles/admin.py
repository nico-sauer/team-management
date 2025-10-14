from django.contrib import admin

from .forms import *
# Register your models here.
from .models import *

admin.site.register(StaffProfile)
admin.site.register(AthleteProfile)
