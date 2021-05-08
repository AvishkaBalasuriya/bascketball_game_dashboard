from django.db.models import Manager
from django.contrib.auth.models import BaseUserManager

from .query_sets import OTPQuerySet


# Overriding model manager to extend it's functionality. So we can add custom query sets to the model and reduce
# Code rewriting
class OtpModelManager(Manager):
    def get_query_set(self):
        return OTPQuerySet(self.model, using=self._db)

    def get_data_by_email(self, email, otp):
        return self.get_query_set().get_data_by_email(email, otp)

    def get_data_by_otp_id_and_email(self, email, id):
        return self.get_query_set().get_data_by_otp_id_and_email(email, id)


# Customizing django's User Manager to work with new custom user model. So we can create super users with django
# management commands. Without this it will not work
class UserManager(BaseUserManager):
    def create_user(self, email, password, first_name, last_name):
        if not email:
            raise ValueError('Email must be provided')
        if not password:
            raise ValueError("Password must be provided")

        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.is_active = True
        user.is_coach = False
        user.is_player = False
        user.save()

        return user

    def create_superuser(self, email, password, first_name, last_name):
        user = self.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        return user
