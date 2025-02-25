from django.db import models
from django.utils import timezone
import pytz
from datetime import datetime

# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    username = models.CharField(max_length=10)
    password1 = models.CharField(max_length=128)
    password2 = models.CharField(max_length=128)
    signup_time = models.TimeField()
    signup_date = models.DateField(default=timezone.now)

    def save(self, *args, **kwargs):
        india_timezone = pytz.timezone("Asia/Kolkata")
        self.signup_time = datetime.now(india_timezone).time()  # sets time in India timezone
        super(Student, self).save(*args, **kwargs)

    def __Str__(self):
        return f"{self.name}{self.phone}{self.email}"
    
class Login(models.Model):
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=60)
    login_datetime = models.DateTimeField(auto_now_add=True)  # Automatically set on creation

class CodeSnippet(models.Model):
    code = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Snippet {self.id}"

class CodeSnippet(models.Model):
    language = models.CharField(
        max_length=50, 
        choices=[("python", "Python"), ("javascript", "JavaScript")],
        default="python"  # ✅ Add a default value
    )
    code = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Snippet ({self.language}) - {self.created_at}"