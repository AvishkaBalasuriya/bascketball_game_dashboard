from django.contrib.auth.hashers import check_password
from django.contrib.auth import login

from authentication.models import User


# This authentication backend is to deal with email password login.
class EmailPasswordAuthenticationBackend:
    def authenticate(self, request, email=None, password=None):
        try:
            email = request.data["email"] if request else email
            password = request.data["password"] if request else password

            user = User.objects.get(email=email)

            # Check if user is active
            if user.is_active:

                # Checking user provided password with database password by hashing and comparing
                password_match_result = check_password(password, user.password)

                # Sending user object if user is valid
                if password_match_result:
                    return user
                else:
                    return None
            elif not user.is_active:
                return None

        # Currently I'm sending None to all errors. Later we can use error codes to send specific errors

        # If provided user email is not in the system, sending error
        except User.DoesNotExist:
            return None

    def get_user(self, email):
        try:
            return User.objects.get(pk=email)
        except User.DoesNotExist:
            return None
