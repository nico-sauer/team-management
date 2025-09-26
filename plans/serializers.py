from rest_framework import serializers
from .models import TrainingPlan, NutritionPlan, MedicalPlan

class TrainingPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingPlan
        fields = '__all__'
        
class NutritionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = NutritionPlan
        fields = '__all__'
        
class MedicalPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalPlan
        fields = '__all__'