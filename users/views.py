from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required, permission_required
from .models import CustomUser, Team

# CustomUser = get_user_model()


@login_required
@permission_required('users.add_customuser', raise_exception=True)
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
        
    return render(request, 'registration/register.html', {'form':form})
        
        
def login_user(request):
    
    if request.method == "POST":
        
        email = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(email = email, password = password)    
        if user is not None: 
            login(request, user)
            return redirect("/")#after login return to Home page
        else:
            messages.error(request, "There was an error. Try to log in again")
            return render(request, 'registration/login.html') #changed redirection
    else: 
         return render(request, 'registration/login.html') 
    
        
def logout_user(request):
    # if request.method == "POST":
    logout(request)
    messages.success(request, "You were logged out.")
    return render(request, "registration/logged_out.html") #redirect("/") I've created separete html page for logged out user
        
def change_password():
    pass

