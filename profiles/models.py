import datetime
from uuid import uuid4

from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
#from model_utils.managers import InheritanceManager, QueryManager
from phonenumber_field.modelfields import PhoneNumberField

from users.models import CustomUser

#from django import forms


#from users.models import [user models]

# Create your models here.

#when creating profiles connect with corresponding user 

ROLE_CHOICES =(
    
    ("Manager", "Manager"),
    ("Trainer", "Trainer"),
    ("Physical Therapist", "Physical Therapist"),
    ("Dietician", "Dietician"),
    ("Doctor", "Doctor"),
    ("Chef", "Chef"),
)

TITLE = (
    ("Dr.", "Dr."),
    ("PhD", "PhD",)
)


BLOOD_TYPES = ( 
            ("", "Select Blood Group"),
            ("A+", "A+"),
            ("A-", "A-"),
            ("B+", "B+"),
            ("B-", "B-"),
            ("O+", "O+"),
            ("O-", "O-"),
            ("AB+", "AB+"),
            ("AB-", "AB-"),
)

GENDER = ( 
            ("", "Select Gender"),
            ("Female", "Female"),
            ("Male", "Male"),
            ("Other", "Other"),
)
    
    
class StaffProfile(models.Model):
   
    #id = models.UUIDField(primary_key=True, default=uuid4)
    icon = models.ImageField(default='default.jpg', upload_to='profile_images')
    title = models.CharField(choices= TITLE, blank=True)
    first_name = models.CharField(("First Name"), max_length=30)
    last_name = models.CharField(("Last Name"), max_length=30)
    birthday = models.DateField(null=True, blank=True)
    slug = AutoSlugField(always_update=True, populate_from="get_full_name", unique=True)

    email = models.EmailField(("Email Address"))
    phone_number = PhoneNumberField("Phone Number")
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null= True, blank=True)

    role = models.CharField(choices = ROLE_CHOICES, blank=True)
    # i've changed def__str__ to one, cause it's showing only last one if there were many and it was a phone_number
    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_phone_number(self):
        return f"{self.phone_number}"
    
    
  
    
class AthleteProfile(models.Model):
    
    #basic profile info:
    
    #id = models.UUIDField(primary_key=True, default=uuid4)
    icon = models.ImageField(default='default.jpg', upload_to='profile_images')
    first_name = models.CharField(("First Name"), max_length=30)
    last_name = models.CharField(("Last Name"), max_length=30)
    slug = AutoSlugField(always_update=True, populate_from="get_full_name", unique=True)
    birthday = models.DateField(null=True, blank=True)
    email = models.EmailField(("Email Address"))
    phone_number = PhoneNumberField("Phone Number")
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    number = models.PositiveIntegerField(default=0, null=True, blank=True) 
    position = models.CharField(null=True, blank=True)
    
    #medical profile info:
    gender = models.CharField(choices = GENDER, blank=True)
    height = models.DecimalField(decimal_places=2, max_digits=5, blank=True, null=True)
    weight = models.DecimalField(decimal_places=2, max_digits=5, blank=True, null=True) 
    blood_type = models.CharField(choices = BLOOD_TYPES, blank=True)
    allergies = models.TextField(blank=True, null=True)

    prescriptions = models.TextField(blank=True)
    treatment_details = models.TextField(blank=True)
    
    diagnoses = models.TextField(blank=True, null=True)
    medical_history = models.TextField(blank=True, null=True)
    additional_notes = models.TextField(blank=True, null=True)
   
    last_updated = models.DateField(auto_now=True) 
    
    
    #nutrition profile info:
    calories = models.CharField(null=True, blank=True)
    protein = models.CharField(null=True, blank=True)
    carbs = models.CharField(null=True, blank=True)
    fat = models.CharField(null=True, blank=True)
    dietary_restrictions = models.TextField(null=True, blank=True)
    
    #medical_records = QueryManager()
    
    def __str__(self):
        return f"{self.get_full_name()} #{self.number}"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
   
    def get_nutri_plan(self):
        return f"TDEE: {self.calories} - Protein: {self.protein} - Carbs: {self.carbs} - Fat: {self.fat}"
    
    def get_phone_number(self):
        return f"{self.phone_number}"

    def get_age(self):
        if self.birthday != None:
            age = datetime.date.today()-self.birthday
            return int((age).days/365.25)
        
