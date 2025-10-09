from django.urls import path
from .views import *
from . import views



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
    path("addsession", views.addmeal, name="addsession"),
    path("addmealplan", views.addmealplan, name="addmealplan"),
    path("addtrainingschedule", views.addmealplan, name="addtrainingschedule"),
    path("deletemeal", views.deletemeal, name="deletemeal"),
    path("deletefromplan", views.deletefromplan, name="deletefromplan"),
    path("dashboard", views.mealplan, name="dashboard"),
]
