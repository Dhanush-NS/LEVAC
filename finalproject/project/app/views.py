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
    if request.user.is_authenticated:
        return render(request,'base.html',{'user':request.user})
    else:

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
            if Student.objects.filter(email=email).exists() or User.objects.filter(email=email).exists():
                messages.error(request, 'Email is registered already, please log in.')
                return redirect('signup')
            
            elif Student.objects.filter(username=username).exists() or User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken, please choose another.')
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
            messages.error(request, "Passwords do not match.")
            return redirect('signup')
    else:
        return render(request, 'REG/signup.html')



def login_view(request):
    if request.method == "POST":
        username = request.POST.get("login_username")
        password = request.POST.get("password") 
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            loginvalue = Login(username=username,password=password)
            loginvalue.save()
            return redirect("base")  # Redirect to the desired page
        else:
            print("Authentication failed")
            messages.error(request, "Invalid credentials. Please try again.")
            return redirect("login")
    else:
        return render(request, "REG/login.html")
    
def edit_view(request):
    if request.method == "POST":
        new_username = request.POST.get("edit_username")  # The new username
        
        # Check if the new username already exists
        if User.objects.filter(username=new_username).exists():
            messages.error(request, "Username already exists, choose another")
            return redirect('edit')
        else:
            user = request.user
            old_username = user.username
            
            # Update the current user's username
            user.username = new_username
            user.save()

            # Update the Student record if it exists
            try:
                student = Student.objects.get(username=old_username)
                student.username = new_username
                student.save()
                messages.success(request, "Profile updated successfully")
            except Student.DoesNotExist:
                messages.error(request, "Student record does not exist.")
        
        return redirect('base')

    return render(request, 'REG/edit.html')

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