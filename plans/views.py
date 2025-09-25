from rest_framework import generics
from .models import TrainingPlan, NutritionPlan, MedicalPlan
from .serializers import TrainingPlanSerializer, NutritionPlanSerializer, MedicalPlanSerializer
from .permissions import IsCreatorOrReadOnly
from django.views.generic.edit import CreateView
from .models import UniversalPlan
from .forms import UniversalPlanForm 

from django.views.generic import TemplateView # we will move it to the core app later
class HomePageView(TemplateView): #
    template_name = 'home.html' #

# API view for listing and creating TrainingPlan objects.
# - GET: Returns a list of all training plans.
# - POST: Allows creation of a new training plan (only for allowed roles).
class TrainingPlanListCreateView(generics.ListCreateAPIView):
    queryset = TrainingPlan.objects.all()
    serializer_class = TrainingPlanSerializer
    permission_classes = [IsCreatorOrReadOnly]  # Custom permission for role-based access

class NutritionPlanListCreateView(generics.ListCreateAPIView):
    queryset = NutritionPlan.objects.all()
    serializer_class = NutritionPlanSerializer
    permission_classes = [IsCreatorOrReadOnly]  

class MedicalPlanListCreateView(generics.ListCreateAPIView):
    queryset = MedicalPlan.objects.all()
    serializer_class = MedicalPlanSerializer
    permission_classes = [IsCreatorOrReadOnly]  
    
class UniversalPlanCreateView(CreateView):
    model = UniversalPlan
    form_class = UniversalPlanForm
    template_name = 'plans/universalplan_form.html'
    success_url = '/success_url/'

