import os
import re
import requests
import google.generativeai as genai
from .models import Student, Login
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import auth, User
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth import logout as auth_logout
from django.conf import settings
from django.http import JsonResponse
from .models import CodeSnippet  
import subprocess
from django.views.decorators.csrf import csrf_exempt


def save_code(request):
    if request.method == "POST":
        language = request.POST.get("language")
        code = request.POST.get("code")
        
        # Save code in the database
        snippet = CodeSnippet.objects.create(
            language=language, 
            code=code,
            user=request.user if request.user.is_authenticated else None
        )

        return JsonResponse({"message": "Code saved successfully", "id": snippet.id})

def run_code(request):
    if request.method == "POST":
        code = request.POST.get("code")
        language = request.POST.get("language")

        if language == "python":
            try:
                result = subprocess.run(["python", "-c", code], capture_output=True, text=True, timeout=5)
                return JsonResponse({"output": result.stdout, "error": result.stderr})
            except subprocess.TimeoutExpired:
                return JsonResponse({"output": "", "error": "Execution timeout!"})

        return JsonResponse({"output": "", "error": "Unsupported language"})

    return JsonResponse({"error": "Invalid request"}, status=400)
    

genai.configure(api_key=settings.GOOGLE_GENAI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro-latest')
chat = model.start_chat(history=[])

def chat_view(request):
    if request.method == 'POST':
        user_input = request.POST.get('message')
        try:
            response = chat.send_message(user_input)
            return JsonResponse({'response': response.text})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return render(request, 'chat.html')

@login_required
@never_cache
def base(request):
    return render(request,'base.html')

def mainpage(request):
    if request.user.is_authenticated:
        try:
            student = Student.objects.get(username=request.user.username)
            return render(request, 'base.html', {'user': request.user, 'student': student})
        except Student.DoesNotExist:
            return render(request, 'base.html', {'user': request.user})
    else:
        return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        profile_photo = request.FILES.get("profile_photo")

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
                
                if profile_photo:
                    student.profile_photo = profile_photo
                
                student.save()

                return redirect('login')

        else:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')
    else:
        return render(request, 'REG/signup.html')


@csrf_exempt
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
    
@login_required
def edit_view(request):
    user = request.user  # Get the currently logged-in user

    # Try to get the student record for this user
    try:
        student = Student.objects.get(username=user.username)
    except Student.DoesNotExist:
        student = None

    if request.method == "POST":  # If the form is submitted
        new_username = request.POST.get("edit_username")  # Get the new username from the form
        new_name = request.POST.get("edit_name")  # Get the new name from the form
        new_photo = request.FILES.get("profile_photo")  # Get uploaded profile photo if any

        # Validate that the new_name is not empty
        if not new_name:
            messages.error(request, "Name cannot be empty.")
            return redirect('edit')

        # Check if the new username already exists (unless it's the current username)
        if User.objects.filter(username=new_username).exists() and new_username != user.username:
            messages.error(request, "Username already exists, choose another")
            return redirect('edit')

        else:
            old_username = user.username  # Save the old username

            # Update the current user's username
            user.username = new_username
            user.save()

            # Update the Student record if it exists
            if student:   
                student.username = new_username
                student.name = new_name
                
                # Process profile photo if uploaded
                if new_photo:
                    student.profile_photo = new_photo
                
                student.save()
                messages.success(request, "Profile updated successfully")
            else:
                messages.error(request, "Student record does not exist.")
        
        return redirect('base')

    return render(request, 'REG/edit.html', {'student': student})

# Logout view to logout user
@never_cache
def logout(request):
    # Logout user and clear session
    auth_logout(request)
    request.session.flush()  # Ensure all session data is cleared
    # messages.success(request, "You have been logged out successfully.")
    return redirect("mainpage")

#*******************************************tutor views
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
def dsa(request):
    return render(request,'DSA/dsa.html')


# ************************************* video views
@login_required
def javavideo(request):
    return render(request,'JAVA/javavideo.html')

@login_required
def cvideo(request):
    return render(request,'C/cvideo.html')

@login_required
def pyvideo(request):
    return render(request,'PYTHON/pyvideo.html')


@login_required
def jsvideo(request):
    return render(request,'JS/jsvideo.html')

@login_required
def dsavideo(request):
    return render(request,'DSA/dsavideo.html')

@login_required
def cppvideo(request):
    return render(request,'CPP/cppvideo.html')

@login_required
def hackerrank(request):
    return render(request,'HACKERRANK/hackerrank.html')

@login_required
def editor(request):
    return render(request,'editor.html')

@login_required
def profile_view(request):
    """View to display user profile information"""
    try:
        student = Student.objects.get(username=request.user.username)
        return render(request, 'REG/profile.html', {'student': student})
    except Student.DoesNotExist:
        messages.error(request, "Profile not found")
        return redirect('base')