from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db import models

from .models import CustomUser, Team

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email", "is_staff", "is_active", "team_id")
    list_filter = ("is_staff", "is_active", "team_id")
    fieldsets = (
        (None, {"fields": ("email", "password", "team_id")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_staff", "is_active", "team_id")}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Team)