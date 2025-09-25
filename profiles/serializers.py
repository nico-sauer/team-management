from rest_framework import serializers

from .models import AthleteProfile, StaffProfile


# general profile serializers -> basically what the athletes mostly see of other profiles
class StaffProfileSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField()
    title = serializers.ReadOnlyField()
    full_name = serializers.ReadOnlyField(source="get_full_name")
    email = serializers.ReadOnlyField()
    phone_number = serializers.ReadOnlyField(source="get_phone_number")
    birthday = serializers.ReadOnlyField()
    role = serializers.ReadOnlyField()

    class Meta:
        model = StaffProfile
        fields = [
            "id",
            #"icon",
            "title",
            "full_name",
            "email",
            "phone_number",
            "birthday",
            "role",
            "appointment"
        ]
       

class AthleteProfileSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField()
    full_name = serializers.ReadOnlyField(source="get_full_name")
    email = serializers.ReadOnlyField()
    phone_number = serializers.ReadOnlyField(source="get_phone_number")
    birthday = serializers.ReadOnlyField()
    age = serializers.ReadOnlyField(source="get_age")
    number = serializers.ReadOnlyField()

    class Meta:
        model = AthleteProfile
        fields = [
            "id",
            #icon",
            "full_name",
            "birthday",
            "age",
            "email",
            "phone_number",
            "number",
            
        ]
       
#serializers for staff access --> refine later with more clarity on what is needed

class ManagerAccessStaffSerializer(serializers.HyperlinkedModelSerializer):

    full_name = serializers.ReadOnlyField(source="get_full_name")
    
    class Meta:
        model = StaffProfile
        fields = [
            #"icon",
            "id",
            "title",
            "full_name",
            "first_name",
            "last_name",
            #"birthday",
            "email",
            "phone_number",
            "role",
            
        ]
      

class ManagerAccessAthleteSerializer(serializers.HyperlinkedModelSerializer):

    full_name = serializers.ReadOnlyField(source="get_full_name")
    height = serializers.ReadOnlyField()
    weight = serializers.ReadOnlyField()
    training_plan = serializers.ReadOnlyField()
    meal_plan = serializers.ReadOnlyField()
    nutri_plan = serializers.ReadOnlyField(source="get_nutri_plan")
    age = serializers.ReadOnlyField(source="get_age")

    class Meta:
        model = AthleteProfile
        fields = [
            #"icon",
            "id",
            "full_name",
            "first_name",
            "last_name",
            "birthday",
            "age",
            "email",
            "phone_number",
            "number",
            "height",
            "weight",
            "training_plan",
            "nutri_plan",
            "meal_plan",
        ]
       
        
class MedicalStaffAccessSerializer(serializers.HyperlinkedModelSerializer):
    
    id = serializers.ReadOnlyField()
    full_name = serializers.ReadOnlyField(source="get_full_name")
    email = serializers.ReadOnlyField()
    phone_number = serializers.ReadOnlyField(source="get_phone_number")
    birthday = serializers.ReadOnlyField()
    age = serializers.ReadOnlyField(source="get_age")
    number = serializers.ReadOnlyField()
    training_plan = serializers.ReadOnlyField()
    meal_plan = serializers.ReadOnlyField()
    nutri_plan = serializers.ReadOnlyField(source="get_nutri_plan")


    class Meta:
        model = AthleteProfile
        fields = [
            "id",
            #"icon",
            "full_name",
            # "first_name",
            # "last_name",
            "birthday",
            "age",
            "email",
            "phone_number",
            "number",
            "height",
            "weight",
            "nutri_plan",
            "training_plan",
            "meal_plan",
            "medical_records",
        ]
            
class TrainerAccessSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField()
    full_name = serializers.ReadOnlyField(source="get_full_name")
    email = serializers.ReadOnlyField()
    phone_number = serializers.ReadOnlyField(source="get_phone_number")
    birthday = serializers.ReadOnlyField()
    age = serializers.ReadOnlyField(source="get_age")
    number = serializers.ReadOnlyField()
    height = serializers.ReadOnlyField()
    weight = serializers.ReadOnlyField()
    meal_plan = serializers.ReadOnlyField()
    nutri_plan = serializers.ReadOnlyField(source="get_nutri_plan")

    class Meta:
        model = AthleteProfile
        fields = [
            #"icon",
            "id",
            "full_name",
            "email",
            "phone_number",
            "number",
            "height",
            "weight",
            "nutri_plan",
            "training_plan",
            "meal_plan",
            
        ]
       
class DieticianAccessSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField()
    full_name = serializers.ReadOnlyField(source="get_full_name")
    email = serializers.ReadOnlyField()
    phone_number = serializers.ReadOnlyField(source="get_phone_number")
    birthday = serializers.ReadOnlyField()
    number = serializers.ReadOnlyField()
    height = serializers.ReadOnlyField()
    weight = serializers.ReadOnlyField()
    training_plan = serializers.ReadOnlyField()
    meal_plan = serializers.ReadOnlyField()

    class Meta:
        model = AthleteProfile
        fields = [
            "id",
            #"icon",
            "full_name",
            "birthday",
            "email",
            "phone_number",
            "number",
            "height",
            "weight",
            "calories",
            "protein",
            "carbs",
            "fat",
            "meal_plan",
            "training_plan"
        ]
       
class ChefAccessSerializer(serializers.HyperlinkedModelSerializer):
    
    id = serializers.ReadOnlyField()
    full_name = serializers.ReadOnlyField(source="get_full_name")
    number = serializers.ReadOnlyField()
    nutri_plan = serializers.ReadOnlyField(source="get_nutri_plan")
    birthday = serializers.ReadOnlyField()
    

    class Meta:
        model = AthleteProfile
        fields = [
            "id",
            #"icon",
            "full_name",
            "birthday",
            "number",
            "nutri_plan",
            "meal_plan"  
        ]
       