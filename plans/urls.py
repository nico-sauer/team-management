from django.urls import path
from .views import TrainingPlanListCreateView, NutritionPlanListCreateView, MedicalPlanListCreateView
from .views import UniversalPlanCreateView


# API endpoints for creating and listing plans
urlpatterns = [
    # Endpoint for training plans (list and create)
    path('training/', TrainingPlanListCreateView.as_view(), name='training-list-create'),
    # Endpoint for nutrition plans (list and create)
    path('nutrition/', NutritionPlanListCreateView.as_view(), name='nutrition-list-create'),
    # Endpoint for medical plans (list and create)
    path('medical/', MedicalPlanListCreateView.as_view(), name='medical-list-create'),
    # Endpoint for creating a universal plan via a form
    path('plan/create/', UniversalPlanCreateView.as_view(), name='universal-plan-create'),
]