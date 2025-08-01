# accounts/backends.py

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    """
    Authenticate using email instead of username.
    """
    def authenticate(self, request, email=None, password=None, **kwargs):
        print(f"🔒 EmailBackend: Trying login with email={email}")
        print("🔒 Custom EmailBackend Called")
        print("Request:", request)
        print("Email:", email)
        print("Password:", password)
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            print("No user found.")
            return None

        if user.check_password(password):
            print("Password correct.")
            return user

        print("Password incorrect.")
        return None
