from django.db import models

class TrainingPlan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class NutritionPlan(models.Model):
    name = models.CharField(max_length=100)
    meals = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class MedicalPlan(models.Model):
    name = models.CharField(max_length=100)
    treatment_details = models.TextField(help_text="Describe the treatment, medications, and instructions for use.")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
#TODO add athlete field when Member model is ready    
class UniversalPlan(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=50, choices=[
        ('coach', 'Coach'),
        ('dietitian', 'Dietitian'),
        ('physiotherapist', 'Physiotherapist'),
        ('manager', 'Manager'),
    ]) #TODO add all of profiles.
    instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    #athlete = models.ForeignKey('members.Member', on_delete=models.CASCADE, null=True, blank=True)  # Assuming a Member model exists in members app
    
    def __str__(self):
        return self.name