from django.shortcuts import get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .forms import StaffRoles, StaffTitle
from .models import AthleteProfile, StaffProfile
from .serializers import * 

# Create your views here.

#manager viewsets

class ManagerAccessAthleteViewSet(viewsets.ModelViewSet):

    queryset = AthleteProfile.objects.all()
    serializer_class = ManagerAccessAthleteSerializer
    http_method_names = ["list", "post","get", "put","head"]
    #permission_classes = [IsAdminUser]
    #authentication_classes = [TokenAuthentication] 
    
    # def get_permissions(self):
    #     if self.action in ["create", "retrieve"]:
    #         permission_classes = [AllowAny]
    #     else:
    #         permission_classes = [AllowAny] #change later
    #     return [permission() for permission in permission_classes]
    
            
    def athlete_detail(request, pk):
        try:
            AthleteProfile = AthleteProfile.objects.get(pk=pk)
        except AthleteProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = AthleteProfileSerializer(AthleteProfile)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = AthleteProfileSerializer(AthleteProfile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            AthleteProfile.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        
class ManagerAccessStaffViewSet(viewsets.ModelViewSet):

    queryset = StaffProfile.objects.all()
    serializer_class = ManagerAccessStaffSerializer
    form_class = StaffRoles
    #permission_classes = [IsAdminUser]
    #authentication_classes = [TokenAuthentication]
    
    def staff_detail(request, pk):
        try:
            StaffProfile = StaffProfile.objects.get(pk=pk)
        except StaffProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = StaffProfileSerializer(StaffProfile)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = StaffProfileSerializer(StaffProfile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            StaffProfile.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
           
        
class MedicalStaffAccess(viewsets.ModelViewSet):

    queryset = AthleteProfile.objects.all()
    serializer_class = MedicalStaffAccessSerializer
    http_method_names = ["get", "put",]

    #permission_classes = [IsAdminUser]
    #authentication_classes = [TokenAuthentication]    
       
    def athlete_detail(request, pk):
        try:
            AthleteProfile = AthleteProfile.objects.get(pk=pk)
        except AthleteProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = AthleteProfileSerializer(AthleteProfile)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = AthleteProfileSerializer(AthleteProfile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class DieticianAccess(viewsets.ModelViewSet):

    queryset = AthleteProfile.objects.all()
    serializer_class = DieticianAccessSerializer
    http_method_names = ["get", "put",]

    #permission_classes = [IsAdminUser]
    #authentication_classes = [TokenAuthentication]    
       
    def athlete_detail(request, pk):
        try:
            AthleteProfile = AthleteProfile.objects.get(pk=pk)
        except AthleteProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = AthleteProfileSerializer(AthleteProfile)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = AthleteProfileSerializer(AthleteProfile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class TrainerAccess(viewsets.ModelViewSet):

    queryset = AthleteProfile.objects.all()
    serializer_class = TrainerAccessSerializer
    http_method_names = ["get", "put",]

    #permission_classes = [IsAdminUser]
    #authentication_classes = [TokenAuthentication]    
       
    def athlete_detail(request, pk):
        try:
            AthleteProfile = AthleteProfile.objects.get(pk=pk)
        except AthleteProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = AthleteProfileSerializer(AthleteProfile)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = AthleteProfileSerializer(AthleteProfile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChefAccess(viewsets.ModelViewSet):

    queryset = AthleteProfile.objects.all()
    serializer_class = ChefAccessSerializer
    http_method_names = ["get", "put",]

    #permission_classes = [IsAdminUser]
    #authentication_classes = [TokenAuthentication]    
       
    def athlete_detail(request, pk):
        try:
            AthleteProfile = AthleteProfile.objects.get(pk=pk)
        except AthleteProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = AthleteProfileSerializer(AthleteProfile)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = AthleteProfileSerializer(AthleteProfile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#viewsets for what the players would see

class StaffViewSet(viewsets.ModelViewSet):

    queryset = StaffProfile.objects.all()
    serializer_class = StaffProfileSerializer
    http_method_names = ["get", "put",]
    
    def staff_detail(request, pk):
        try:
            StaffProfile = StaffProfile.objects.get(pk=pk)
        except StaffProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = StaffProfileSerializer(StaffProfile)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = StaffProfileSerializer(StaffProfile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

    
class AthleteViewSet(viewsets.ModelViewSet):

    queryset = AthleteProfile.objects.all()
    serializer_class = AthleteProfileSerializer
    http_method_names = ["get", "put",]