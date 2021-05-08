from django.utils import timezone

from rest_framework import serializers

from datetime import timedelta
from uuid import uuid4

from .models import User, OtpDetails, UserStat
from .utils import generate_otp_code, send_email
from game.models import Coach, Player


# This serializer is use to update user password
class UserPasswordUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password")

    def update(self, instance, validated_data):
        instance.set_password(validated_data["password"])
        instance.save()
        return instance


# This serializer is used to create a new user
class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password", "first_name", "last_name")

    def validate(self, data):

        # Getting user type by validating coach_id,player_id,is_admin fields in request
        coach_id = self.context['request']["coach_id"] if "coach_id" in self.context['request'] else None
        player_id = self.context['request']["player_id"] if "player_id" in self.context['request'] else None
        is_admin = self.context['request']["is_admin"] if "is_admin" in self.context['request'] else False

        # Setting default values
        self.context["player"] = None
        self.context["coach"] = None
        self.context["is_admin"] = False

        # If user account type is coach, Getting particular coach instance from the database
        if coach_id:
            try:
                coach = Coach.objects.get(id=coach_id)
                self.context["coach"] = coach
                return data
            except Coach.DoesNotExist:
                # Raising validation error if provided coach id is invalid
                raise serializers.ValidationError("Provided coach id is invalid")

        # If user account type is player, Getting particular player instance from the database
        elif player_id:
            try:
                player = Player.objects.get(id=player_id)
                self.context["player"] = player
                return data
            except Player.DoesNotExist:
                # Raising validation error if provided player id is invalid
                raise serializers.ValidationError("Provided player id is invalid")

        # If user account type is admin, setting is_admin as True
        elif is_admin:
            self.context["is_admin"] = is_admin
            return data

        else:
            # Raising validation error if request not met any account type
            raise serializers.ValidationError("Please specify coach_id,player_id or is_admin")

    # Saving user into the database
    def save(self, **kwargs):
        user = User(
            email=self.data["email"],
            first_name=self.data["first_name"],
            last_name=self.data["last_name"],
            coach=self.context["coach"],
            player=self.context["player"],
            is_admin=self.context["is_admin"]
        )
        user.set_password(self.data["password"])
        user.save()
        return user


# This serializer is use to create new OTP code and send that to the user
class OTPCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtpDetails
        fields = ("user",)

    def save(self, **kwargs):

        # Getting user instance from the context data and email from request data
        user = self.context["user"]

        # Getting all records for the user in otp_details table. l
        recent_otp_codes = OtpDetails.objects.filter(user__email=user.email)

        # If there is no any records, sending new OTP code to the user
        if recent_otp_codes.count() == 0:
            return self.send_otp(user)

        # If there is any record for the user, Looping through them and check whether if there is any active OTP code
        # is available for the user. Later on we can create a cron job to change is_active status according to the
        # code expiration. So we can directly query OtpDetails.objects.filter(user=user,is_active=False) therefore we
        # don't want to use loop here
        for recent_otp_code in recent_otp_codes:
            # If there is otp code which is not expired, return None to send error to the user
            if not recent_otp_code.is_expired:
                return None

        return self.send_otp(user)

    def send_otp(self, user):
        otp_code = generate_otp_code()
        email_result = send_email("Password reset",
                                  "Please use below OTP code to reset your password. \n {}".format(otp_code),
                                  "avishkabalasuriya980330@gmail.com", user.email)
        if email_result:
            otp_details = OtpDetails(id=str(uuid4()), user=user, otp_code=otp_code,
                                     expire_date=timezone.now() + timedelta(minutes=2))
            otp_details.save()
            return True
        else:
            return False


class UserStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStat
        fields = ("user", "last_activity", "time_spent", "login_count", "is_online",)
