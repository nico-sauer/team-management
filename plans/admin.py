from django.contrib import admin
from .models import TrainingPlan, NutritionPlan, MedicalPlan, UniversalPlan

admin.site.register([TrainingPlan, NutritionPlan, MedicalPlan, UniversalPlan])
