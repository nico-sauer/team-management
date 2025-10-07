from django.contrib import admin
# from .models import TrainingPlan, NutritionPlan, MedicalPlan, UniversalPlan

# admin.site.register([TrainingPlan, NutritionPlan, MedicalPlan, UniversalPlan])


from .models import Meals, TDEE, TrainingSessions

# Register your models here.

#admin.site.register(User)
admin.site.register(Meals)
admin.site.register(TrainingSessions)
admin.site.register(TDEE)
