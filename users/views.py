from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm, FirstCustomUserCreationForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.template.loader import render_to_string
import os
from django.contrib.auth.models import Permission
from django.conf import settings

def first_registration(request):
    if request.method == 'POST':
        form = FirstCustomUserCreationForm(request.POST)

        try:
            if form.is_valid():
                user = form.save()
                # add the permission to the manager to add new users
                # if user.role == "Manager":
                #     permission = Permission.objects.get(codename="add_customuser")
                #     user.user_permissions.add(permission)
                # user.save()
                messages.success(request, "Registration successful!")
                # send a confirmation email
                registered_name = form.cleaned_data["first_name"]
                registered_email = form.cleaned_data["email"]
                html = render_to_string(
                    "registration/emails/registersuccess.html",
                    {
                        "name": registered_name,
                        "email": registered_email,
                    },
                )
                send_mail(
                    subject="Team Management App Registration",
                    message="You registerd succesfully to our app",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[
                        f"{registered_email}",
                    ],
                    html_message=html,
                )
                return redirect("users:login")
        except ValidationError:
            messages.error(
                request, "The team is already exist, please enter a new team"
            )
            form = FirstCustomUserCreationForm()
    else:
        form = FirstCustomUserCreationForm()    
    return render(request, 'registration/first_register.html', {'form':form})
    
        


@login_required
@permission_required("users.add_customuser", raise_exception=True)
def register_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(
                                      data=request.POST,
                                      current_user=request.user
                                      )
        if form.is_valid():
            user = form.save()
            messages.success(request, "User registered successfully!")
            # send a confirmation email
            registered_name = form.cleaned_data["first_name"]
            registered_email = form.cleaned_data["email"]
            html = render_to_string(
                "registration/emails/registersuccess.html",
                {
                    "name": registered_name,
                    "email": registered_email,
                },
                )
            send_mail(
                    subject="Team Management App Registration",
                    message="You registerd succesfully to our app",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[
                        f"{registered_email}",
                    ],
                    html_message=html,
                )
            return redirect('/')  # Redirect to home page after registration
        else:
            # Clear previous messages before adding a new error
            storage = messages.get_messages(request)
            for _ in storage:
                pass  # This clears the message queue
            messages.error(request, "There was an error in the registration, please try again")

    else:
        form = CustomUserCreationForm(current_user=request.user)
    return render(request, 'registration/register.html', {'form': form})
        
        
def login_user(request):

    if request.method == "POST":

        email = request.POST["email"]
        password = request.POST["password"]

        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in.")
            return redirect("/")  # after login return to Home page
        else:
            messages.error(request, "There has been an error. Try to log in again")
            return redirect("/")
    else:
        return render(
            request, "registration/login.html"
        )  # add the template to login and render


def logout_user(request):
    # if request.method == "POST":
    logout(request)
    messages.success(request, "You were logged out.")
    return redirect("/")
        


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()

            update_session_auth_hash(
                request, user
            )  # keep user logged in after change password
            messages.success(request,
                             "Your password was successfully updated!"
                             )
            return redirect("/")  # return the user to his profile
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "registration/change_password.html", {"form": form})
