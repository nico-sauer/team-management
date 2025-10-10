from django.urls import path
from .views import *
from . import views

#app_name = "plans" # added app_name for namespacing

# API endpoints for creating and listing plans
urlpatterns = [
    # Endpoint for training plans (list and create)
    # path('training/', TrainingPlanListCreateView.as_view(), name='training-list-create'),
    # # Endpoint for nutrition plans (list and create)
    # path('nutrition/', NutritionPlanListCreateView.as_view(), name='nutrition-list-create'),
    # # Endpoint for medical plans (list and create)
    # path('medical/', MedicalPlanListCreateView.as_view(), name='medical-list-create'),
    # # Endpoint for creating a universal plan via a form
    # path('plan/create/', UniversalPlanCreateView.as_view(), name='universal-plan-create'),
    path("", views.index, name="index"),
    # path("login", views.login_view, name="login"),
    # path("logout", views.logout_view, name="logout"),
    # path("register", views.register, name="register"),
    path("tdee", views.tdee, name="tdee"),
    path("addmeal", views.addmeal, name="addmeal"),
    path("addsession", views.addsession, name="addsession"),
    path("addmealplan", views.addmealplan, name="addmealplan"),
    path("addtrainingschedule", views.addtrainingschedule, name="addtrainingschedule"),
    path("deletemeal", views.deletemeal, name="deletemeal"),
    path("deletefromplan", views.deletefromplan, name="deletefromplan"),
    path("deletesession", views.deletesession, name="deletesession"),
    path("deletefromschedule", views.deletefromschedule, name="deletefromschedule"),
    path("dashboard", views.mealplan, name="dashboard"),
    path("mealplan", views.mealplan, name="mealplan"),
]

