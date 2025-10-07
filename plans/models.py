from django.db import models

# class TrainingPlan(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return self.name

# class NutritionPlan(models.Model):
#     name = models.CharField(max_length=100)
#     meals = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return self.name
    
# class MedicalPlan(models.Model):
#     name = models.CharField(max_length=100)
#     treatment_details = models.TextField(help_text="Describe the treatment, medications, and instructions for use.")
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return self.name
    
# #TODO add athlete field when Member model is ready    
# class UniversalPlan(models.Model):
#     name = models.CharField(max_length=100)
#     role = models.CharField(max_length=50, choices=[
#         ('coach', 'Coach'),
#         ('dietitian', 'Dietitian'),
#         ('physiotherapist', 'Physiotherapist'),
#         ('manager', 'Manager'),
#     ]) #TODO add all of profiles.
#     instructions = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     #athlete = models.ForeignKey('members.Member', on_delete=models.CASCADE, null=True, blank=True)  # Assuming a Member model exists in members app
    
#     def __str__(self):
#         return self.name



from django.contrib.auth.models import AbstractUser
from django.db import models

#from users.models import User
# class User(AbstractUser):
#     pass


class Meals(models.Model):
    name = models.TextField(max_length=50, blank=True, null=True)
    totalfat = models.PositiveIntegerField(default=0)
    totalcarb = models.PositiveIntegerField(default=0)
    totalprotein = models.PositiveIntegerField(default=0)
    calories = models.PositiveIntegerField(default=0)
    #chef= models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True) # or just user when we have roles etc 



class WeeklyMealPlan(models.Model):
    day = models.TextField(max_length=10)
    meal = models.ForeignKey(Meals, on_delete=models.CASCADE, blank=True, null=True)
    #user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)



class TrainingSessions(models.Model):
    name = models.TextField(max_length=50, blank=True, null=True)
    type = models.CharField(blank=True, null=True) # choices or just examples as placeholder
    description = models.TextField(max_length=2500, default="", blank=True, null=True)
    #  trainer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)#user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

class WeeklySessions(models.Model):
    day = models.TextField(max_length=10)
    session = models.ForeignKey(TrainingSessions, on_delete=models.CASCADE, blank=True, null=True)
    #user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)


#calculate tdee (undecided if necessary tbh)
class TDEE(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    calories = models.PositiveIntegerField(default=0)