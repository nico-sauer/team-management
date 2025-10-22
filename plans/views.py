# from rest_framework import generics
# from .models import TrainingPlan, NutritionPlan, MedicalPlan
# from .serializers import TrainingPlanSerializer, NutritionPlanSerializer, MedicalPlanSerializer
# from .permissions import IsCreatorOrReadOnly
# from django.views.generic.edit import CreateView
# from .models import UniversalPlan
# from .forms import UniversalPlanForm 
 #

# # API view for listing and creating TrainingPlan objects.
# # - GET: Returns a list of all training plans.
# # - POST: Allows creation of a new training plan (only for allowed roles).
# class TrainingPlanListCreateView(generics.ListCreateAPIView):
#     queryset = TrainingPlan.objects.all()
#     serializer_class = TrainingPlanSerializer
#     permission_classes = [IsCreatorOrReadOnly]  # Custom permission for role-based access

# class NutritionPlanListCreateView(generics.ListCreateAPIView):
#     queryset = NutritionPlan.objects.all()
#     serializer_class = NutritionPlanSerializer
#     permission_classes = [IsCreatorOrReadOnly]  

# class MedicalPlanListCreateView(generics.ListCreateAPIView):
#     queryset = MedicalPlan.objects.all()
#     serializer_class = MedicalPlanSerializer
#     permission_classes = [IsCreatorOrReadOnly]  
    
# class UniversalPlanCreateView(CreateView):
#     model = UniversalPlan
#     form_class = UniversalPlanForm
#     template_name = 'plans/universalplan_form.html'
#     success_url = '/success_url/'




from appointments.views import *

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import *
from users.models import CustomUser

def index(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("dashboard"))

    else:
        return render(request, "registration/login.html")



class Dashboard(generic.ListView):
    model = Booking
    
    template_name = "plans/dashboard.html"

    """create context-dict =
                        {"object_list":"[]",
                         "prev-month": "",
                         "next-month":"",
                         calendar:""} """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date/month for the calendar
        d = get_date(self.request.GET.get("month", None))
        context["prev_month"] = prev_month(d)
        context["next_month"] = next_month(d)

        # timeframe: full month
        first_day = d.replace(day=1)
        last_day = first_day + timedelta(
            days=calendar.monthrange(d.year, d.month)[1] - 1
        )

        # get all bookings
        bookings = Booking.objects.all()
        all_sessions = TrainingSessions.objects.filter()
        weekly_sessions = WeeklySessions.objects.filter().order_by("time")
        all_meals = Meals.objects.filter()
        weekly_meals = WeeklyMealPlan.objects.filter()
        

        # list of occurences
        expanded_events = []
        for booking in bookings:
            occurrences = booking.get_occurrences(first_day, last_day)
            for occ in occurrences:
                expanded_events.append((occ, booking))

        # Instantiate our calendar class with today's year, date and occurences
        cal = Calendar(d.year, d.month, events=expanded_events)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context= {
            "calendar": mark_safe(html_cal),
            "all_sessions": all_sessions,
            
            "weekly_sessions": weekly_sessions,
            "all_meals": all_meals,
            
            "weekly_meals": weekly_meals,
            }
            
        return context

def addmeal(request):
    if not request.user.is_authenticated:
        return redirect('users:login') #redirect to login if not authenticated

    if request.method == "GET":
        # TODO this will change to if user is authenticated as a chef basically
        
        if request.user.is_authenticated: 
            all_meals = Meals.objects.filter(chef = request.user)
            no_user = False
        else:
            all_meals = None
            no_user = True

        context = {
            "all_meals": all_meals,
            "no_user": no_user
        }

        return render(request, "plans/addmealplan.html", context)
    else:
        mealtitle = request.POST.get("mealtitle")
        carb_grams = request.POST.get("carbgrams")
        fat_grams = request.POST.get("fatgrams")
        protein_grams = request.POST.get("proteingrams")
        calories = request.POST.get("calories")
        dietary_requirements = request.POST.get("dietreq")

        # If required field missing, show error or re-render form
        if not mealtitle:
            all_meals = Meals.objects.filter(chef=request.user)
            context = {
                "all_meals": all_meals,
                "error": "Meal title is required."
            }
            return render(request, "plans/addmeal.html", context)

        # default to zero
        if not carb_grams:
            carb_grams = 0
        if not fat_grams:
            fat_grams = 0
        if not protein_grams:
            protein_grams = 0
        if not calories:
            calories = 0
     
        # define variables to save in meal model
        chef = request.user
        name = mealtitle

     

        # save meal
        meal = Meals(name = name, totalcarb = carb_grams, totalfat = fat_grams, totalprotein = protein_grams, calories = calories, dietary_requirements = dietary_requirements, chef = chef)
        meal.save()
        all_meals = Meals.objects.filter(chef = request.user)

        context = {
            "all_meals": all_meals
        }

        return render(request, "plans/addmealplan.html", context)

def deletemeal(request):
    all_meals = Meals.objects.filter(chef=request.user)
    meal_id = request.POST.get("mealtodelete")
    try:
        meal_to_delete = Meals.objects.get(pk=meal_id)
        if meal_to_delete.chef != request.user: # check if the meal belongs to the user
            return HttpResponseNotFound("You do not have permission to delete this meal.")
        meal_to_delete.delete()
    except Meals.DoesNotExist: # exception if ID not found
        return HttpResponseNotFound("Meal not found")

    context = {
        "all_meals": all_meals
    }
    return render(request, "plans/addmealplan.html", context)

def addmealplan(request):
    
     # TODO change to if user is authenticated as a chef again

    user = request.user 
    macros = {}
    percentage = {}

    if request.method == "GET":

        # query that user's meals
        if request.user.is_authenticated:
            all_meals = Meals.objects.filter(chef = user)
            weekly_meals = WeeklyMealPlan.objects.filter(user = user)

            # calculate macros/percentage
            macros = calculate_macros(weekly_meals)
            percentage = calculate_percentage(macros)

            no_user = False
        else:
            all_meals = None
            weekly_meals = None
            macros = None
            percentage = None
            no_user = True

        context = {
            "all_meals": all_meals,
            "no_user": no_user,
            "weekly_meals": weekly_meals,
            "macros": macros,
            "percentage": percentage
        }

        return render(request, "plans/addmealplan.html", context)

    else:

        
        if request.user.is_authenticated:
            all_meals = Meals.objects.filter(chef = request.user)
            no_user = False
        else:
            all_meals = None
            no_user = True

        # get form inputs for weekly meal plan model
        day = request.POST.get("day")
        meal_id = request.POST["meal_select"]
        meal_select = Meals.objects.get(pk = meal_id)
        user = request.user

    
        weekly = WeeklyMealPlan(day = day, meal = meal_select, user = user)
        weekly.save()

        weekly_meals = WeeklyMealPlan.objects.filter(user = request.user)

        # calculate macros
        macros = calculate_macros(weekly_meals)
        percentage = calculate_percentage(macros)

        context = {
            "all_meals": all_meals,
            "no_user": no_user,
            "weekly_meals": weekly_meals,
            "macros": macros,
            "percentage": percentage
        }

        return render(request, "plans/addmealplan.html", context)

def mealplan(request):
    #basic view just to check mealplan without editing rights for anyone who isnt role chef
    user = request.user
    macros = {}
    percentage = {}

    if request.method == "GET":

        # query that user's meals
        if request.user.is_authenticated:
            all_meals = Meals.objects.filter(chef = user)
            weekly_meals = WeeklyMealPlan.objects.filter(user = user)

            #calculate macros and percentage
            macros = calculate_macros(weekly_meals)
            percentage = calculate_percentage(macros)

            no_user = False
        else:
            all_meals = None
            weekly_meals = None
            macros = None
            percentage = None
            no_user = True

        context = {
            "all_meals": all_meals,
            "no_user": no_user,
            "weekly_meals": weekly_meals,
            "macros": macros,
            "percentage": percentage
        }

        return render(request, "plans/mealplan.html", context)
    
def deletefromplan(request):
    meal_id = request.POST.get("mealtodelete")
    try: #check if meal exists
        meal_object = Meals.objects.get(pk=meal_id)
    except Meals.DoesNotExist:
        return HttpResponseNotFound("Meal not found")
    daydelete = request.POST.get("daydelete")

    meal_to_delete = WeeklyMealPlan.objects.filter(meal=meal_object, user=request.user, day=daydelete)
    object_to_delete = meal_to_delete.first()
    if object_to_delete:
        object_to_delete.delete()

    all_meals = Meals.objects.filter(chef = request.user)
    weekly_meals = WeeklyMealPlan.objects.filter(user = request.user)

    # calculate macros again
    macros = calculate_macros(weekly_meals)
    percentage = calculate_percentage(macros)

    context = {
        "all_meals": all_meals,
        "monday_meals": all_meals,
        "weekly_meals": weekly_meals,
        "macros": macros,
        "percentage": percentage
    }

    return render(request, "plans/addmealplan.html", context)

def calculate_macros(weekly_meals):

    weekly_fat = 0
    weekly_carb = 0
    weekly_protein = 0
    weekly_calories = 0

    for meal in weekly_meals:

        weekly_fat = weekly_fat + meal.meal.totalfat
        weekly_carb = weekly_carb + meal.meal.totalcarb
        weekly_protein = weekly_protein + meal.meal.totalprotein
        weekly_calories = weekly_calories + meal.meal.calories

    average_fat = round(weekly_fat / 7)
    average_carb = round(weekly_carb / 7)
    average_protein = round(weekly_protein / 7)
    average_calories = round(weekly_calories / 7)

    macros = {
        "average_fat": average_fat,
        "average_carb": average_carb,
        "average_protein": average_protein,
        "average_calories": average_calories,
    }

    return macros

def calculate_percentage(macros):

    calories_from_fat = macros.get("average_fat") * 9
    calories_from_carb = macros.get("average_carb") * 4
    calories_from_protein = macros.get("average_protein") * 4
    calories = macros.get("average_calories")

    if calories == 0:
        percentage = {
            "fat": 33,
            "carb": 33, 
            "protein": 33
        }

    else:
        fat = round((calories_from_fat / calories) * 100)
        carb = round((calories_from_carb / calories) * 100)
        protein = round((calories_from_protein / calories) * 100)
        
        percentage = {
            "fat": fat,
            "carb": carb, 
            "protein": protein
        }

    return percentage
    


# training schedule

def addsession(request):

    # TODO change basic user authentications to trainer role
    if request.method == "GET":

        # query that user's meals
        if request.user.is_authenticated:
            all_sessions = TrainingSessions.objects.filter(trainer = request.user)
            no_user = False
        else:
            all_sessions = None
            no_user = True

        context = {
            "all_sessions": all_sessions,
            "no_user": no_user
        }

        return render(request, "plans/addtrainingschedule.html", context)

    else:

        # get inputs from form
        name = request.POST["trainingtitle"]
        description = request.POST["description"]
        type = request.POST.get("type") #choices between cross-training like strength, cardio, flexibility 
                                                        #and whatever you call training the actual sport. maybe typing in the type would be better
        
    
        trainer = request.user
        # name = trainingtitle
        # description =  trainingdescription
        # type = trainingtype
       
    
        # save training
        session = TrainingSessions(name = name, type = type, description = description, trainer = trainer)
        session.save()

        
        all_sessions = TrainingSessions.objects.filter(trainer = request.user)
        #print(all_sessions)

        context = {
            "all_sessions": all_sessions
        }

        return render(request, "plans/addtrainingschedule.html", context)

def deletesession(request):

    # query that user's meals
    all_sessions = TrainingSessions.objects.filter(trainer = request.user)

    # Find session by id and delete from TrainingSessions object
    trainingsessions_id = request.POST.get("sessiontodelete")
    session_to_delete = TrainingSessions.objects.get(pk=trainingsessions_id)
    session_to_delete.delete()

    context = {
        "all_sessions": all_sessions
    }

    return render(request, "plans/addtrainingschedule.html", context)

def addtrainingschedule(request):
    
    # TODO change to trainer role 

    user = request.user
   

    if request.method == "GET":

        #
        if request.user.is_authenticated:
            all_sessions = TrainingSessions.objects.filter(trainer = user)
            weekly_sessions = WeeklySessions.objects.filter(user = user).order_by("time")
            no_user = False
        else:
            all_sessions = None
            weekly_sessions = None
            no_user = True

        context = {
            "all_sessions": all_sessions,
            "no_user": no_user,
            "weekly_sessions": weekly_sessions,
            
        }

        return render(request, "plans/addtrainingschedule.html", context)

    else:

        
        if request.user.is_authenticated:
            all_sessions = TrainingSessions.objects.filter(trainer = request.user)
            no_user = False
        else:
            all_sessions = None
            no_user = True

    
        day = request.POST.get("day")
        time = request.POST.get("time")
        trainingsessions_id = request.POST["session_select"]
        session_select = TrainingSessions.objects.get(pk = trainingsessions_id)
        user = request.user

        
        # save to weekly schedule
        weekly = WeeklySessions(day = day, time = time, session = session_select, user = user)
        weekly.save()

        weekly_sessions = WeeklySessions.objects.filter(user = request.user).order_by("time")

      

        context = {
            "all_sessions": all_sessions,
            "no_user": no_user,
            "weekly_sessions": weekly_sessions,

        }

        return render(request, "plans/addtrainingschedule.html", context)

def trainingschedule(request):
    #view just to check mealplan without editing rights so anyone who is authenticated as part of the team
    user = request.user
    

    if request.method == "GET":

        # query that user's meals
        if request.user.is_authenticated:
            all_sessions = TrainingSessions.objects.filter(trainer = user)
            weekly_sessions = WeeklySessions.objects.filter(user = user).order_by("time")

            no_user = False
        else:
            all_sessions = None
            weekly_sessions = None
            no_user = True

        context = {
            "all_sessions": all_sessions,
            "no_user": no_user,
            "weekly_sessions": weekly_sessions,
            
        }

        return render(request, "plans/trainingschedule.html", context)
    
def deletefromschedule(request):

    trainingsessions_id = request.POST.get("sessiontodelete")
    session_object = TrainingSessions.objects.get(pk = trainingsessions_id)
    daydelete = request.POST.get("daydelete")

    session_to_delete = WeeklySessions.objects.filter(session = session_object, user = request.user, day = daydelete)
    object_to_delete = session_to_delete.first()
    object_to_delete.delete()

   
    all_sessions = TrainingSessions.objects.filter(trainer = request.user)
    weekly_sessions = WeeklySessions.objects.filter(user = request.user)

 

    context = {
        "all_sessions": all_sessions,
        "monday_sessions": all_sessions,
        "weekly_sessions": weekly_sessions,
    }

    return render(request, "plans/addtrainingschedule.html", context)

    
def tdee(request):
    context = {
        "calories": "2000"
    }
    return render(request, "plans/tdee.html", context)