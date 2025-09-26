from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required, permission_required
from .models import CustomUser, Team
# from profiles.models import staffprofile


# CustomUser = get_user_model()

@login_required
@permission_required('auth.add_user', raise_exception=True)
def register_user(request):
    
    # current_user = request.user give the info of the logged in user
    # user_id = current_user.id give the id of the logged in user
    # manager_team= staffprofile.objects.get(pk=user_id).filter(team_id)
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
            
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful!")
            return redirect("home")
         
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'register.html', {'form':form})
        
        
def login_user(request):
    
    if request.method == "POST":
        
        email = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(email = email, password = password)    
        if user is not None: 
            login(request, user)
            return redirect("/")
        else:
            messages.success(request, "There was an error. Try to log in again")
            return redirect('login')
    else: 
         return render(request,'registration/login.html') #add the template to login and render 
    
        
def logout_user(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "You were logged out.")
        return redirect("/")
        
        
        