
import datetime
from uuid import uuid4
from users.models import CustomUser
from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
#from model_utils.managers import InheritanceManager, QueryManager
from phonenumber_field.modelfields import PhoneNumberField

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
    icon = models.ImageField#(default='default.jpg', upload_to='profile_images')
    title = models.CharField(choices= TITLE, blank=True)
    first_name = models.CharField(("First Name"), max_length=30)
    last_name = models.CharField(("Last Name"), max_length=30)
    #birthday = models.DateField(null=True, blank=False)
    slug = AutoSlugField(always_update=True, populate_from="get_full_name", unique=True)

    email = models.EmailField(("Email Address"))
    phone_number = PhoneNumberField("Phone Number")
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    role = models.CharField(choices = ROLE_CHOICES, blank=True)
    
    def __str__(self):
        full_name = self.get_full_name()
        return full_name
    
    def __str__(self):
        phone_number = self.get_phone_number()
        return phone_number

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_phone_number(self):
        return f"{self.phone_number}"
    
    
  
    
class AthleteProfile(models.Model):
    
    #basic profile info:
    
    #id = models.UUIDField(primary_key=True, default=uuid4)
    icon = models.ImageField#(default='default.jpg', upload_to='profile_images')
    first_name = models.CharField(("First Name"), max_length=30)
    last_name = models.CharField(("Last Name"), max_length=30)
    slug = AutoSlugField(always_update=True, populate_from="get_full_name", unique=True)
    birthday = models.DateField(null=True, blank=False)

    email = models.EmailField(("Email Address"))
    phone_number = PhoneNumberField("Phone Number")
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    number = models.PositiveIntegerField(default=0) #unless we use their jersey number as id for easier searching
    position = models.CharField(null=True)
    
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
   
    last_updated = models.DateField(null=True, blank=True)
    
    
    #nutrition profile info:
    calories = models.CharField(null=True)
    protein = models.CharField(null=True)
    carbs = models.CharField(null=True)
    fat = models.CharField(null=True)
    dietary_restrictions = models.TextField(null=True)
    
    meal_plan = models.TextField(null=True)
    training_plan = models.TextField(null=True)
    
    #medical_records = QueryManager()
    
    def __str__(self):
        full_name = self.get_full_name()
        return full_name
    
    def __str__(self):
        phone_number = self.get_phone_number()
        return phone_number
    
    def __str__(self):
        nutri_plan = self.get_nutri_plan()
        return nutri_plan

    def __str__(self):
        age = self.get_age()
        return age
    
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
        
    # def get_records(self):
    #     for i in MedicalRecordsData.medical_records():
    #         return list(MedicalRecords))

# class MedicalRecords(AthleteProfile):
#     pass
    #athlete = models.ForeignKey(AthleteProfile, related_name='medical_records', on_delete=models.CASCADE, blank=True)#TextField(blank=True)#ManyToManyField("self", symmetrical=False) # through="AthleteProfile", through_fields=("medical_records"))#.ForeignKey(AthleteProfile, on_delete=models.CASCADE, related_name="medical_records")
    # prescriptions = models.TextField(blank=True)
    # treatment_details = models.TextField(blank=True)
    # last_updated = models.DateField(null=True, blank=True)
    # allergies = models.TextField(blank=True, null=True)
    # diagnoses = models.TextField(blank=True, null=True)
    #past_records = models.ForeignKey("MedicalRecordsArchive", related_name='medical_records', on_delete=models.CASCADE)
    #slug = AutoSlugField(always_update=True, populate_from="get_full_name", unique=True)
    # class Meta:
    #     ordering = ["-last_updated"]
    
    # def __str__(self):
    #     return f"{self.athlete}"
    # def __str__(self):
    #     medical_records = self.get_records()
    #     return medical_records
    
    # def get_records(self):
        
    #     records = {AthleteProfile: record for record in instance}
    #     return list(records)
   
#     class MedicalRecordsArchive(models.Model):
#         pass
# #       medical_records = models.ForeignKey(MedicalRecordsArchive, related_name='medical_records', on_delete=models.CASCADE)
    
