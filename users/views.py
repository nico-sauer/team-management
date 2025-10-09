from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm, FirstCustomUserCreationForm
from django.contrib.auth.decorators import login_required, permission_required
from .models import CustomUser, Team
from django.contrib.auth.models import Group
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


#add email after user registration
#check how to move group/team/role from the customuser. first user(group=managers, role=manager)
#added user (team = manager's team)



def first_registration(request):

    if request.method == 'POST':
        form = FirstCustomUserCreationForm(request.POST)
            
        if form.is_valid():
    
            form.save()
            #send a confirmation email
            messages.success(request, "Registration successful!")
            return redirect("home")
            
    else:
        form = FirstCustomUserCreationForm()
        
    return render(request, 'registration/register.html', {'form':form})



@login_required
@permission_required('users.add_customuser', raise_exception=True)
def register_user(request):
    # if no teams exist, use the FirstCustomUserCreationForm
    if Team.objects.count() == 0:
        form_class = FirstCustomUserCreationForm
    else:
        form_class = CustomUserCreationForm

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful!")
            return redirect("home")
    else:
        form = form_class()
    return render(request, 'registration/register.html', {'form': form})
        
        
def login_user(request):
    
    if request.method == "POST":
        
        email = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(email = email, password = password)    
        if user is not None: 
            login(request, user)
            return redirect("/")#after login return to Home page
        else:
            messages.success(request, "There was an error. Try to log in again")
            return redirect('/')
    else: 
         return render(request,'registration/login.html') #add the template to login and render 
    
        
def logout_user(request):
    # if request.method == "POST":
    logout(request)
    messages.success(request, "You were logged out.")
    return redirect("/")
        
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
                
            update_session_auth_hash(request, user)  #keep user logged in after change password
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile') #return the user to his profile
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })

