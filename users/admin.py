from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db import models


from .models import CustomUser, Team
# from .forms import UserCreationForm

    
admin.site.register(Team)
admin.site.register(CustomUser)




admin.site.register(CustomUser)