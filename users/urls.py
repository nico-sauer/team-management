
from django.urls import path, include
from . import views

app_name = "users"

urlpatterns = [
    #path("", include("django.contrib.auth.urls"))
    path("register/", views.register_user, name="register"),
    path("login_user/", views.login_user, name="login"),
    path("logout_user/", views.logout_user, name="logout"),
    path("change_password/", views.change_password, name="change_password"),
    path("first_registration/", views.first_registration, name="first_registration")
    
]

#add to settings.py:
# LOGIN_REDIRECT_URL = "/"

# LOGOUT_REDIRECT_URL = "/"