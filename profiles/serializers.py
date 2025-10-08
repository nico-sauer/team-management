from rest_framework import serializers

from .models import AthleteProfile, MedicalRecords, StaffProfile

#from plans.models import MedicalRecords


# class MedicalRecordsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MedicalRecords
#         fields = "__all__"
        #exclude = ["id", "athlete"]
    
    # def get_records(self, instance):
    #     try:
    #         medical_records = {record.id:record for record in instance}
    #         return list(medical_records)
    #     except AssertionError:
    #       return f"No records."
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
    position = serializers.ReadOnlyField()
    
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
            "position",
            
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
      

class ManagerAccessAthleteSerializer(serializers.ModelSerializer):

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
            "position",
            "height",
            "weight",
            "training_plan",
            "nutri_plan",
            "meal_plan",
        ]

# class MedicalRecordsDataSerializer(serializers.HyperlinkedModelSerializer):
#     medical_records = serializers.ReadOnlyField()   
#     class Meta:
#         model = MedicalRecordsData
#         fields = ["medical_records"]
        
#     records_list = []
#     for i, records in enumerate(medical_records.objects.all()):
#         records.medical_records = name_list[i]
#         records_list.append(records)

# MedicalRecordsDataSerializer(obj_list, many=True).data
        
class MedicalRecordsSerializer(serializers.ModelSerializer):
    
    # id = serializers.ReadOnlyField()
    full_name = serializers.ReadOnlyField(source="get_full_name")
    email = serializers.ReadOnlyField()
    phone_number = serializers.ReadOnlyField(source="get_phone_number")
    # birthday = serializers.ReadOnlyField()
    age = serializers.ReadOnlyField(source="get_age")
    # number = serializers.ReadOnlyField()
    # position = serializers.ReadOnlyField()
    # training_plan = serializers.ReadOnlyField()
    # meal_plan = serializers.ReadOnlyField()
    nutri_plan = serializers.ReadOnlyField(source="get_nutri_plan")
    #last_updated =serializers.ReadOnlyField()
    #medical_records = serializers.ReadOnlyField()


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
            "gender",
            "email",
            "phone_number",
            "number",
            "position",
            "height",
            "weight",
            "nutri_plan",
            "training_plan",
            "meal_plan",
           # "medical_records",
            "blood_type",
            "allergies",
            #"dietary_restrictions",
            "prescriptions",
            "treatment_details",
            "diagnoses",
            #"medical_history",
            "additional_notes",
            "last_updated",
        ]
            
class TrainerAccessSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField()
    full_name = serializers.ReadOnlyField(source="get_full_name")
    email = serializers.ReadOnlyField()
    phone_number = serializers.ReadOnlyField(source="get_phone_number")
    birthday = serializers.ReadOnlyField()
    age = serializers.ReadOnlyField(source="get_age")
    number = serializers.ReadOnlyField()
    position = serializers.ReadOnlyField()
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
            "position",
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
    position = serializers.ReadOnlyField()
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
            "position",
            "height",
            "weight",
            "calories",
            "protein",
            "carbs",
            "fat",
            "dietary_restrictions",
            "meal_plan",
            "training_plan"
        ]
       
class ChefAccessSerializer(serializers.HyperlinkedModelSerializer):
    
    id = serializers.ReadOnlyField()
    full_name = serializers.ReadOnlyField(source="get_full_name")
    number = serializers.ReadOnlyField()
    nutri_plan = serializers.ReadOnlyField(source="get_nutri_plan")
    birthday = serializers.ReadOnlyField()
    dietary_restrictions  = serializers.ReadOnlyField()
    

    class Meta:
        model = AthleteProfile
        fields = [
            "id",
            #"icon",
            "full_name",
            "birthday",
            "number",
            "position",
            "dietary_restrictions",
            "nutri_plan",
            "meal_plan"  
        ]
       