from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.db.models import Q

class EmailOrUsernameBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            # Try to get the user by email or username
            user = User.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
