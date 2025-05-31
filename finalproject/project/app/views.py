import os
import re
import requests
import markdown
import bleach
import json
import google.generativeai as genai
from .models import Student,Login
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse ,get_object_or_404
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
import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import ContactForm
from django.core.mail import send_mail
from dotenv import load_dotenv

# Load environment variables before using them
load_dotenv()
# def api_key(request):
#     youtube_api_key = os.getenv('Youtube_api_key')
    
#     # Check if API key exists
#     if not youtube_api_key:
#         print("ERROR: YouTube API key not found in environment variables")
#         return HttpResponse("API key configuration error", status=500)
    
#     print(f"API Key loaded: {youtube_api_key[:10]}...")  # Only print first 10 chars for security
    
#     context = {
#         'youtube_api_key': youtube_api_key
#     }
    
#     return render(request, 'cvideo.html', context)


def check_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': Student.objects.filter(username__iexact=username).exists() or User.objects.filter(username = username).exists()
    }
    return JsonResponse(data)

def check_email(request):
    email = request.GET.get('email', None)
    data = {
        'is_taken': Student.objects.filter(email__iexact=email).exists() or User.objects.filter(email=email).exists()
    }
    return JsonResponse(data)

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        print("Form is valid:", form.is_valid())  # Debug line
        print("Form errors:", form.errors)  # Debug line
        
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            print("Attempting to send email...")  # Debug line
            
            try:
                send_mail(
                    f'New Contact Form Submission from {name}',
                    f'''Name: {name}\nEmail: {email}\nMessage: {message}''',
                    settings.DEFAULT_FROM_EMAIL,
                    ['nsdhanush5@gmail.com'],
                    fail_silently=False,
                )
                print("Email sent successfully!")  # Debug line
                messages.success(request, 'Thank you for contacting us!')
            except Exception as e:
                print("Email failed to send:", str(e))  # Debug line
                messages.error(request, 'Failed to send message. Please try again.')
            
            return redirect('base')
    else:
        form = ContactForm()
    
    return render(request, 'base.html', {'form': form})

def save_code(request):
    if request.method == "POST":
        language = request.POST.get("language")
        code = request.POST.get("code")
        
        # Save code in the database
        snippet = CodeSnippet.objects.create(language=language, code=code)

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
    

# genai.configure(api_key=settings.GOOGLE_GENAI_API_KEY)
# model = genai.GenerativeModel('gemini-2.0-flash')
# chat = model.start_chat(history=[])

# def chat_view(request):
#     if request.method == 'POST':
#         user_input = request.POST.get('message')
#         try:
#             response = chat.send_message(user_input)
#             return JsonResponse({'response': response.text})
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)
#     return render(request, 'chat.html')

# @login_required
# @never_cache
def base(request):
    return render(request,'base.html')

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
    
# @login_required
def edit_view(request):
    user = request.user

    if request.method == "POST":
        try:
            # Get form data
            new_name = request.POST.get("edit_name")
            phone = request.POST.get("phone")
            bio = request.POST.get("bio")
            # pic = request.POST.get("pic")

            # Debug print to check received data
            print(f"Received data - Name: {new_name}, Phone: {phone}, Bio: {bio}")

            # Validate required fields
            if not new_name:
                messages.error(request, "Name cannot be empty.")
                return redirect('edit')

            # Update or create Student record
            student, created = Student.objects.update_or_create(
                username=user.username,
                defaults={
                    'name': new_name,
                    'phone': phone or '',
                    'bio': bio or '',
                    'email': user.email  # Ensure email is always synced
                }
            )
            
            messages.success(request, "Profile updated successfully!")
            return redirect('base')

        except Exception as e:
            messages.error(request, f"Error updating profile: {str(e)}")
            return redirect('edit')

    else:
        # GET request - show form with current data
        try:
            student = Student.objects.get(username=user.username)
        except Student.DoesNotExist:
            # Create empty student record if it doesn't exist
            student = Student(
                username=user.username,
                name=user.get_full_name(),
                email=user.email
            )

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
# @login_required
def python(request):
    return render(request,'PYTHON/python.html')

# @login_required
def c(request):
    return render(request,'C/c.html')
 
# @login_required
def cpp(request):
    return render(request,'CPP/cpp.html')

# @login_required
def js(request):
    return render(request,'JS/js.html')

# @login_required
def java(request):
    return render(request,'JAVA/java.html')


# @login_required
def dsa(request):
    return render(request,'DSA/dsa.html')


# ************************************* video views
# @login_required
def javavideo(request):
    youtube_api_key = os.getenv("youtube_api_key")
    return render(request,'JAVA/javavideo.html',{"youtube_api_key":youtube_api_key})

# @login_required
def cvideo(request):
    youtube_api_key = os.getenv("youtube_api_key")
    return render(request,'C/cvideo.html',{"youtube_api_key":youtube_api_key})

# @login_required
def pyvideo(request):
    youtube_api_key = os.getenv("youtube_api_key")
    return render(request,'PYTHON/pyvideo.html',{"youtube_api_key":youtube_api_key})
    

# @login_required
def jsvideo(request):
    youtube_api_key = os.getenv("youtube_api_key")
    return render(request,'JS/jsvideo.html',{"youtube_api_key":youtube_api_key})

# @login_required
def dsavideo(request):
    youtube_api_key = os.getenv("youtube_api_key")
    return render(request,'DSA/dsavideo.html',{"youtube_api_key":youtube_api_key})

# @login_required
def cppvideo(request):
    youtube_api_key = os.getenv("youtube_api_key")
    return render(request,'CPP/cppvideo.html',{"youtube_api_key":youtube_api_key})

# @login_required
def hackerrank(request):
    return render(request,'HACKERRANK/hackerrank.html')

# @login_required
def editor(request):
    return render(request,'editor.html')
# Rest of your existing code...

'''this section for handling the gemini responses'''

SAMPLE_RESPONSES = {
    'python': "Python is a versatile programming language. Here's a simple example:\n\n```python\ndef greet(name):\n    return f\"Hello, {name}!\"\n\nprint(greet(\"World\"))\n```\n\nWould you like to learn more about Python functions?",
    'javascript': "JavaScript is great for web development. Here's a simple function:\n\n```javascript\nfunction greet(name) {\n    return `Hello, ${name}!`;\n}\n\nconsole.log(greet(\"World\"));\n```\n\nDo you want to know more about JavaScript functions?",
    'java': "Java is widely used for enterprise applications. Here's a simple example:\n\n```java\npublic class HelloWorld {\n    public static void main(String[] args) {\n        System.out.println(\"Hello, World!\");\n    }\n}\n```\n\nWould you like to learn more about Java classes?",
    'help': "I can help you with:\n- Programming concepts\n- Debugging code\n- Learning resources\n- Best practices\n\nWhat specific coding help do you need today?",
}

# Check if Gemini API is available
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

if GEMINI_AVAILABLE and hasattr(settings, 'GEMINI_KEY'):
    genai.configure(api_key=settings.GEMINI_KEY)
else:
    print("Warning: Gemini API not configured properly")


def processed(content):
    """
    Process markdown content to HTML with sanitization
    """
    html = markdown.markdown(
        content,
        extensions=[
            'markdown.extensions.fenced_code',  # Support ```code blocks
            'markdown.extensions.tables',  # Support tables
            'markdown.extensions.codehilite',  # Support syntax highlighting
            'markdown.extensions.nl2br'  # Convert newlines to <br>
        ]
    )

    # Define allowed HTML tags and attributes
    allowed_tags = [
        'p', 'div', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'ul', 'ol', 'li', 'blockquote', 'pre', 'code', 'em',
        'strong', 'del', 'a', 'img', 'br', 'hr', 'table', 'thead',
        'tbody', 'tr', 'th', 'td'
    ]

    allowed_attributes = {
        'a': ['href', 'title', 'target', 'rel'],
        'img': ['src', 'alt', 'title', 'width', 'height'],
        'code': ['class'],
        'pre': ['class', 'data-language'],  # Added data-language for code highlighting
        'span': ['class', 'style'],  # Needed for code highlighting
        'td': ['colspan', 'rowspan', 'align'],
        'th': ['colspan', 'rowspan', 'align'],
        'div': ['class']  # Added for code block container
    }

    # Sanitize HTML to prevent XSS attacks
    clean_html = bleach.clean(
        html,
        tags=allowed_tags,
        attributes=allowed_attributes,
        strip=True
    )
    return clean_html


def process_code_blocks(content):
    """
    Format code blocks in the message content for proper display
    """
    # Look for code blocks with language specification
    pattern = r"```(\w+)?\n([\s\S]*?)```"

    def replacement(match):
        language = match.group(1) or ""
        code = match.group(2)
        return f'<div class="code-block"><pre data-language="{language}">{code}</pre></div>'

    processed_content = re.sub(pattern, replacement, content)
    # Process remaining markdown
    return processed(processed_content)


def chat(request):
    """
    Render the Gemini Assistant page
    """
    # Clear any previous chat history
    if 'chat_history' in request.session:
        del request.session['chat_history']
    
    context = {
        'title': 'LEVAC - Gemini Assistant',
    }
    return render(request, 'chat.html', context)


@csrf_exempt  # Added CSRF exemption for API endpoint
def chat_with_gemini(request):
    """
    API endpoint to handle chat messages with Gemini
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)

    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        print(f"Received message: {user_message}")

        if not user_message:
            return JsonResponse({'error': 'Message is required'}, status=400)
            
        # Save message history in the session for context if needed
        if 'chat_history' not in request.session:
            request.session['chat_history'] = []

        # Add user message to history
        request.session['chat_history'].append({
            'role': 'user',
            'parts': [{'text': user_message}]
        })

        # Get response from Gemini API
        gemini_response = get_gemini_response(user_message, request.session.get('chat_history', []))
        print(f"Generated response: {gemini_response[:100]}...")  # Debug log

        # Add response to chat history
        request.session['chat_history'].append({
            'role': 'model',  # Changed from 'assistant' to 'model' to match API expectations
            'parts': [{'text': gemini_response}]
        })
        request.session.modified = True

        # Process code blocks for proper display
        processed_response = process_code_blocks(gemini_response)

        return JsonResponse({
            'success': True,
            'message': gemini_response,
            'processed_message': processed_response
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        print(f"Error in chat_with_gemini: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)


def get_gemini_response(message, history=None):
    """
    Generate a response using Gemini API or sample responses
    """
    # If Gemini API is available and configured, use it
    if GEMINI_AVAILABLE and hasattr(settings, 'GEMINI_KEY') and settings.GEMINI_KEY:
        try:
            print("Using Gemini API for response")
            
            # Configure the model
            model = genai.GenerativeModel("gemini-2.0-flash")
            
            # Format history correctly for the API
            api_history = []
            if history:
                # Convert session history format to API format
                for entry in history:
                    role = entry.get('role')
                    parts = entry.get('parts', [])
                    if role and parts:
                        api_history.append({
                            'role': 'user' if role == 'user' else 'model',
                            'parts': parts
                        })
            
            # Start a chat with history if available
            if api_history:
                chat = model.start_chat(history=api_history)
            else:
                chat = model.start_chat()
                
            # Send message and get response
            response = chat.send_message(message)
            return response.text

        except Exception as e:
            print(f"Error using Gemini API: {str(e)}")
            # Fall back to sample responses

    # If API is not available or there was an error, use sample responses
    message_lower = message.lower()
    print("Using sample responses")

    # Check for keywords in the message and return appropriate response
    for keyword, response in SAMPLE_RESPONSES.items():
        if keyword in message_lower:
            return response

    # Default response if no keywords match
    return "I'm here to help with your coding questions. Could you provide more details about what you'd like to learn or what problem you're trying to solve?"