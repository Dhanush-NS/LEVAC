import os
import re
import requests
import google.generativeai as genai
from .models import Student,Login
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import auth, User
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth import logout as auth_logout


def mainpage(request):
    return render(request,'index.html')


def signup(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 == password2:
            if Student.objects.filter(email=email).exists():
                messages.info(request, 'Email is registered already, please log in.')
                return redirect('signup')
            
            elif Student.objects.filter(username=username).exists():
                messages.info(request, 'Username is already taken, please choose another.')
                return redirect('signup')

            else:
                # Create User object
                user = User.objects.create_user(username=username, 
                                                email=email, 
                                                password=password1)
                user.save()

                # Create Student object and associate with the User
                student = Student(name=name, 
                                  phone=phone, 
                                  email=email, 
                                  username=username, 
                                  password1=password1, 
                                  password2=password2)
                student.save()

                return redirect('login')

        else:
            messages.info(request, "Passwords do not match.")
            return redirect('signup')
    else:
        return render(request, 'signup.html')




def login(request):
    if request.method == "POST":
        email = request.POST.get("loginemail")
        password = request.POST.get("loginpassword")
        
        user = auth.authenticate(email = email, password=password)

        # If user is authenticated then login user
        if user is not None:
            auth.login(request, user)
            # Save login record in Login model
            applogin = Login(email=email, password=password)
            applogin.save()

            # Redirect to home page
            return redirect("base")
        else:

            # If user is not authenticated then show error message
            # and redirect to login page
            messages.info(request, "Invalid Credential")
            return redirect("login")
    else:
        # If request is not post then render login page
        return render(request, "login.html")
    
       

@login_required
@never_cache
def base(request):
    return render(request,'base.html')


# Logout view to logout user
@never_cache
def logout(request):
    # Logout user and clear session
    auth_logout(request)
    request.session.flush()  # Ensure all session data is cleared
    messages.success(request, "You have been logged out successfully.")
    return redirect("mainpage")


@login_required
def python(request):
    return render(request,'PYTHON/python.html')

@login_required
def c(request):
    return render(request,'C/c.html')
 
@login_required
def cpp(request):
    return render(request,'CPP/cpp.html')

@login_required
def js(request):
    return render(request,'JS/js.html')

@login_required
def java(request):
    return render(request,'JAVA/java.html')

@login_required
def pyvideo(request):
    return render(request,'PYTHON/pyvideo.html')

@login_required
def javavideo(request):
    return render(request,'JAVA/javavideo.html')

@login_required
def cvideo(request):
    return render(request,'C/cvideo.html')

@login_required
def jsvideo(request):
    return render(request,'JS/jsvideo.html')

@login_required
def dsavideo(request):
    return render(request,'DSA/dsavideo.html')