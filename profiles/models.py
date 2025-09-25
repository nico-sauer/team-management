import datetime
from uuid import uuid4

from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

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
    
    #user = models.OneToOneField(User, on_delete=models.CASCADE)

    role = models.CharField(choices = ROLE_CHOICES, blank=True)
    appointment = models.CharField(null=True) #placeholder
    
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
    
    #id = models.UUIDField(primary_key=True, default=uuid4)
    icon = models.ImageField#(default='default.jpg', upload_to='profile_images')
    first_name = models.CharField(("First Name"), max_length=30)
    last_name = models.CharField(("Last Name"), max_length=30)
    slug = AutoSlugField(always_update=True, populate_from="get_full_name", unique=True)
    birthday = models.DateField(null=True, blank=False)

    email = models.EmailField(("Email Address"))
    phone_number = PhoneNumberField("Phone Number")
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    number = models.PositiveIntegerField(default=0) #unless we use their jersey number as id for easier searching
    
    height = models.DecimalField(decimal_places=2, max_digits=5, blank=True, null=True)
    weight = models.DecimalField(decimal_places=2, max_digits=5, blank=True, null=True) 
    
    
    #nutrition data placeholders etc this can/will be refinded at a later stage with keys etc once we know relations
    #e.g. foreign key fields for plans/records that link to them elsewhere if too long to be reasonable all in one page?
    calories = models.CharField(null=True)
    protein = models.CharField(null=True)
    carbs = models.CharField(null=True)
    fat = models.CharField(null=True)
    meal_plan = models.TextField(null=True)
    training_plan = models.TextField(null=True)
    medical_records = models.TextField(null=True)

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


