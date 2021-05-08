from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.db import models
from django.utils import timezone

from .managers import OtpModelManager, UserManager

from game.models import Coach, Player


class User(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(max_length=255, primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(default=timezone.now)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    coach = models.ForeignKey(Coach, blank=True, null=True, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, blank=True, null=True, on_delete=models.CASCADE)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    class Meta:
        managed = True


class UserStat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_activity = models.DateTimeField()
    login_count = models.PositiveIntegerField(default=0)
    is_online = models.BooleanField(default=False)

    # Using properties to calculate and show time_spent of the user. Later on we can use cached_properties to enhance
    # performance
    @property
    def time_spent(self):
        time_spent = self.last_activity - self.user.last_login
        return float(time_spent.seconds / 60)

    def __str__(self):
        return self.user

    class Meta:
        managed = True


class OtpDetails(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code = models.IntegerField()
    is_active = models.BooleanField(default=True)
    expire_date = models.DateTimeField(default=timezone.now)

    objects = OtpModelManager()

    # Using properties to check if otp is expired and change the is_active status based on that.
    # Later on we can use cached_properties to enhance performance
    @property
    def is_expired(self):
        if timezone.now() > self.expire_date:
            self.is_active = False
            self.save()
            return True
        return False

    class Meta:
        managed = True


'''
    I'm using django's inbuilt signals for user login and user logout to get login count and maintain user online status
'''


def user_login(sender, request, user, **kwargs):
    try:
        user_stat = UserStat.objects.get(user__email=user.email)
        user_stat.is_online = True
        user_stat.login_count += 1
        user_stat.save()
    except UserStat.DoesNotExist:
        try:
            user_stat = UserStat(user=request.user, last_activity=timezone.now(), login_count=0, is_online=True)
            user_stat.save()
        except Exception:
            pass


def user_logout(sender, request, user, **kwargs):
    user_stat = UserStat.objects.get(user__email=user.email)
    user_stat.is_online = False
    user_stat.save()


user_logged_in.connect(user_login)
user_logged_out.connect(user_logout)
