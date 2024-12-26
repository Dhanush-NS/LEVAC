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
                # Hash password before saving
                # hashed_password = make_password(password1)
                user = User.objects.create_user(name=name, 
                                  phone=phone, 
                                  email=email, 
                                  username=username, 
                                  password1=password1,
                                  password2=password2)
                user.save()
                return redirect('login')

                

        else:
            messages.info(request, "Passwords do not match.")
            return redirect('mainpage')
    else:
        return render(request, 'signup.html')



def login(request):
    if request.method == "POST":
        email = request.POST.get("loginemail")
        password = request.POST.get("loginpassword")

        try:
            student = Student.objects.get(email=email)
        except Student.DoesNotExist:
            messages.error(request, "couldn't login, Please signup first...")
            return redirect('login')
        except Student.MultipleObjectsReturned:
            # Handle the case where multiple students with the same email exist
            students = Student.objects.filter(email=email)
            student = students.first()
            
        if student.password1 != password:
            messages.error(request, 'Wrong password')
            return redirect('login')
        # Save login record in Login model
        applogin = Login(email=email, password=password)
        applogin.save()
        # student = Student.objects.get(username)
        student_username = student.username
        # messages.success(request, "Login successful")  # Optional: Add a success message
        return render(request, 'base.html',{'username':student_username})

        # return HttpResponse("Login successful")  # Or redirect to another page

    return render(request, 'login.html')

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



def python(request):
    return render(request,'PYTHON/python.html')


def c(request):
    return render(request,'C/c.html')
 

def cpp(request):
    return render(request,'CPP/cpp.html')


def js(request):
    return render(request,'JS/js.html')


def java(request):
    return render(request,'JAVA/java.html')


def pyvideo(request):
    return render(request,'PYTHON/pyvideo.html')


def javavideo(request):
    return render(request,'JAVA/javavideo.html')



def cvideo(request):
    return render(request,'C/cvideo.html')

def jsvideo(request):
    return render(request,'JS/jsvideo.html')


def dsavideo(request):
    return render(request,'DSA/dsavideo.html')