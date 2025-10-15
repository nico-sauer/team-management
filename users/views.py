from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm, FirstCustomUserCreationForm
from django.contrib.auth.decorators import login_required, permission_required
from .models import CustomUser, Team
from django.contrib.auth.models import Group
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.template.loader import render_to_string
import os
from django.conf import settings

#add email after user registration


# def send_registrtion_email():
#     email = EmailMessage(
#     subject='Welcom to Team Management',
#     body='Hello,you were registered to Team Management App.f'<a href=http://127.0.0.1:8000/</a>',
#     from_email='TeamManagement@example.com',
#     to=['edengoldstein5@gmail.com'],
#         )
#     email.send()
                

def first_registration(request):
    
    if request.method == 'POST':
        form = FirstCustomUserCreationForm(request.POST)
                 
        try: 
            if form.is_valid():
        
                form.save()
                #send a confirmation email
                messages.success(request, "Registration successful!")
                
                registered_name = form.cleaned_data['first_name']
                registered_email = form.cleaned_data['email']
                # registered_team = form.cleaned_data['team_id']
                html = render_to_string('registration/emails/registersuccess.html', {'name':registered_name, 'email':registered_email,})
                send_mail(subject='Team Management App Registration', message=f'{registered_name} Welcome to Team Management! You registered our App succesfully.', from_email=settings.EMAIL_HOST_USER, recipient_list=[f'{registered_email}',], html_message=html)
                return redirect("users:login")
        except ValidationError:
            messages.error(request, "The team is already exist, please enter a new team")
            form = FirstCustomUserCreationForm()
        
                
    else:
        form = FirstCustomUserCreationForm()    
            
    return render(request, 'registration/first_register.html', {'form':form})
    
        


@login_required
@permission_required('users.add_customuser', raise_exception=True)
def register_user(request):
    
    
    
    if request.method == 'POST':
        
        form = CustomUserCreationForm(data=request.POST,current_user=request.user)
        
        
        if form.is_valid():  
                form.save()
           
            
    else:
        form = CustomUserCreationForm(current_user=request.user)
        
    return render(request, 'registration/register.html', {'form':form})
        
        
def login_user(request):
    
    if request.method == "POST":
        
        email = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(email = email, password = password)    
        if user is not None: 
            login(request, user)
            messages.success(request, "You are login")
            return redirect("/")#after login return to Home page
        else:
            messages.error(request, "There was an error. Try to log in again")
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

