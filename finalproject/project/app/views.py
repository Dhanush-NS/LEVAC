from django.shortcuts import render, redirect, HttpResponse
from .models import Student,Login
from django.contrib import messages
import re
import requests
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import auth, User
from django.contrib.auth.hashers import check_password
import os
import google.generativeai as genai

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
                hashed_password = make_password(password1)
                student = Student(name=name, phone=phone, email=email, username=username, password1=hashed_password)
                student.save()
                return redirect('mainpage')

                # Authenticate and log in the user immediately after signup
                # user = authenticate(request, username=username, password=password1)
                # if user is not None:
                #     login(request, user)
                #     messages.success(request, "Signup successful, and you are logged in.")
                #     return redirect('mainpage')

                # else:
                #     messages.error(request, "Authentication failed. Please try again.")
                #     return redirect('signup')

        else:
            messages.info(request, "Passwords do not match.")
            return redirect('mainpage')

    return render(request, 'index.html')


def login(request):
    if request.method == "POST":
        email = request.POST.get("loginemail")
        password = request.POST.get("loginpassword")

        try:
            student = Student.objects.get(email=email)
        except Student.DoesNotExist:
            messages.error(request, "Email not found. Please sign up first.")
            return redirect('mainpage')

        # Authenticate user
        user = authenticate(email = student.email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "Login successful")
            return redirect('pyvideo')  # Redirect to the desired page after login

        else:
            messages.error(request, 'Invalid credentials. Please try again.')
            return redirect('mainpage')

    return render(request, 'index.html')
# Logout view to logout user
def logout(request):

    # Logout user and redirect to home page
    # auth.logout(request)
    return redirect("mainpage")

def python(request):
    return render(request,'python.html')
def c(request):
    return render(request, 'c.html') 
def cpp(request):
    return render(request,'cpp.html')
def js(request):
    return render(request,'js.html')
def java(request):
    return render(request,'java.html')

def pyvideo(request):
    return render(request,'pyvideo.html')
def javavideo(request):
    return render(request,'javavideo.html')
def cvideo(request):
    return render(request,'cvideo.html')
def jsvideo(request):
    return render(request,'jsvideo.html')
def dsavideo(request):
    return render(request,'dsavideo.html')