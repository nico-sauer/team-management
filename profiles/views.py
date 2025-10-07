from django.shortcuts import get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import renderer_classes, api_view
from django.http import HttpResponse
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import render,redirect
from django.contrib import messages
from django.urls import reverse
from django.template import loader
#from .response import render_html_response
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer, StaticHTMLRenderer
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.response import Response
from rest_framework.views import *
from .forms import *
from .models import AthleteProfile, StaffProfile
from django.views.generic import TemplateView
from .serializers import * 
# Create your views here.
# @ team pls ignore this gigantic mess i will clean this up soon
#basic profile views for athletes
def athlete_list(request):
  athletes = AthleteProfile.objects.all().values()
  template = loader.get_template('profiles/athlete_list.html')
  context = {
    'athletes': athletes,
  }
  return HttpResponse(template.render(context, request))


def athlete_details(request, id):
  athlete = AthleteProfile.objects.get(id=id)
  template = loader.get_template('profiles/athlete.html')
  
  context = {
    'athlete': athlete,
  }
  return HttpResponse(template.render(context, request))


def post(request, id):
    template = loader.get_template('profiles/athlete.html')
    athlete = get_object_or_404(AthleteProfile, id=id)
    serializer = MedicalRecordsSerializer(athlete, data=request.data)
    context = {
    'athlete': athlete,
    }
    if not serializer.is_valid():
        return Response({'serializer': serializer, 'profile': athlete})
    serializer.save()
    return HttpResponse(template.render(context, request))

def medical_records(request, id):
    athlete = AthleteProfile.objects.get(id=id)
    if request.method == "POST":
    #template = loader.get_template('profiles/medical_records.html')
        form = AthleteProfileForm(instance=athlete)
        if form.is_valid():
            form.save()
            return redirect('medical-records', athlete(id))
    else:
        form = AthleteProfileForm(instance=athlete)
        
    context = {
    'athlete': athlete,
    'form': form
   }
    # if request.method == "POST":
    return render(request, 'profiles/medical_records.html', context)

  
#   context = {
#     'athlete': athlete,
#   }
#   return HttpResponse(template.render(context, request))

#basic profile views for staff 

def staff_list(request):
  staff = StaffProfile.objects.all().values()
  template = loader.get_template('profiles/staff_list.html')
  context = {
    'staff': staff,
  }
  return HttpResponse(template.render(context, request))


def staff_details(request, id):
  staff_member = StaffProfile.objects.get(id=id)
  template = loader.get_template('profiles/staff.html')
  
  context = {
    'staff_member': staff_member,
  }
  return HttpResponse(template.render(context, request))




    
    

# @api_view(['GET'])
# @renderer_classes([StaticHTMLRenderer])
# def simple_html_view(request):
#     data = '<html><body><h1>Hello, world</h1></body></html>'
#     return Response(data)

# # Create your views here.
class MedicalRecordsView(APIView):
    """
    View to get the listing of all contacts.
    Supports both HTML and JSON response formats.
    """
    serializer_class = MedicalRecordsSerializer
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'profiles/medical_records.html'
    
    


    # def get(self, request, pk):
    #     athlete = get_object_or_404(AthleteProfile, pk=pk)
    #     #self.check_object_permissions(self.request, athlete) # required for IsOwnerOrReadOnly to work fine see https://stackoverflow.com/questions/25554415/django-rest-framework-ignoring-my-isownerorreadonly-permissions
    #     serializer_context = {
    #         'request': AthleteProfile(request),
    #     }
    #     serializer = MedicalRecordsSerializer(athlete, context=serializer_context)
    #     return Response({'serializer': serializer, 'athlete': athlete})

    # def post(self, request, pk):
    #     athlete = get_object_or_404(AthleteProfile, pk=pk)
    #     #self.check_object_permissions(self.request, athlete) # required for IsOwnerOrReadOnly to work fine see https://stackoverflow.com/questions/25554415/django-rest-framework-ignoring-my-isownerorreadonly-permissions
    #     serializer_context = {
    #         'request': AthleteProfile(request),
    #     }
    #     serializer = MedicalRecordsSerializer(athlete, context=serializer_context, data=request.data)
    #     if not serializer.is_valid():
    #         return Response({'serializer': serializer, 'athlete': athlete})
    #     serializer.save()
    #     return HttpResponseRedirect(reverse('MedicalRecords')) # redirect to URL that is associated with the name announces-list

    
    def get(self, request, pk, *args, **kwargs):
        queryset = AthleteProfile.objects.all().values()

        if request.accepted_renderer.format == 'html':
            serializer = self.serializer_class(request.data)  # Create an instance of the serializer
            context = {'athletes': queryset, 'serializer': serializer}
            return render_html_response(context, self.template_name)
        else:
            # Return a JSON response if the format is not HTML
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data)
        
    def post(self, request, *args, **kwargs):
        """
        Handle POST request to add or update a contact.
        """
        message = "Congratulations! your contact has been added successfully."
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            serializer.save()

            if request.accepted_renderer.format == 'html':
                messages.success(request, message)
                return redirect('athletes')

            else:
                # Return JSON response with success message and serialized data
                return Response(status_code=status.HTTP_201_CREATED,
                                    message=message,
                                    data=serializer.data
                                    )
        else:
            # Invalid serializer data
            if request.accepted_renderer.format == 'html':
                # Render the HTML template with invalid serializer data
                context = {'serializer':serializer}
                return render_html_response(context,self.template_name)
            else:   
                # Return JSON response with error message
                return Response(status_code=status.HTTP_400_BAD_REQUEST,
                                    message="We apologize for the inconvenience, but please review the below information.",
                                    data=(serializer.errors))



# def test(request):
    
#     return render(request, "profiles/athleteprofile.html")
# class Dashboard(TemplateView):
#     template_name = 'profiles/dashboard.html'

# def dashboard(request):
#     render(request, "dashboard.html")
    
#     # render(template_name="dashboard.html")
    #return render()
#     template_name = 'dashboard.html'

# def render_to_response(self, context, **response_kwargs):
#     return self.response_class(
#         request=self.request,
#         template=self.get_template_names(),
#         context=context,
#         **response_kwargs,
#     )

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
           
        
class MedicalRecords(viewsets.ModelViewSet):

    queryset = AthleteProfile.objects.all()
    #template_name = "athleteprofile.html"
    serializer_class = MedicalRecordsSerializer
   # renderer_classes = [TemplateHTMLRenderer]
    http_method_names = ["get", "put",]

    #permission_classes = [IsAdminUser]
    #authentication_classes = [TokenAuthentication]    
       
    def medical_records_detail(request, pk):
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


    # if request.method == "GET":

    #     # Query that user's meals
    #     if request.user.is_authenticated:
    #         all_meals = Meals.objects.filter(mealcreator = request.user)
    #         no_user = False
    #     else:
    #         all_meals = None
    #         no_user = True

    #     context = {
    #         "all_meals": all_meals,
    #         "no_user": no_user
    #     }

    #     return render(request, "plans/addmeal.html", context)

  

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
    
    
    
    
    
# def add_athlete(request):
#     return render(request,'add-athlete.html',{'active_page': 'athletes'})   


# # @login_required
# def all_athletes(request):
#     athletes = AthleteProfile.objects.all()
#     return render(request, 'athletes.html', {'athletes': athletes,'active_page': 'athletes'})

# # @login_required
# def add_staff(request):
#     return render(request,'add-staff.html',{'active_page': 'staff'})
# # @login_required
# def all_staff(request):
#     staff = StaffProfile.objects.all()
#     return render(request, 'staff.html', {'staff': staff,'active_page': 'staff'})