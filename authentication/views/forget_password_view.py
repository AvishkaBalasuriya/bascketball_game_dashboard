from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from authentication.models import OtpDetails
from authentication.serializers import UserPasswordUpdateSerializer

import traceback


# This view is to change user password after user successfully validate his/her OTP code
# This is a POST method API and it required email,otp_id,password as it's request data
# This endpoint is allow to anyone
@api_view(["POST"])
@permission_classes([AllowAny])
def forget_password(request):
    response_data = {}
    try:
        email = request.data["email"]
        otp_id = request.data["otp_id"]

        try:
            # Validating OTP ID with our recodes
            otp_details = OtpDetails.objects.get_data_by_otp_id_and_email(email, otp_id)

            # Pass user data to the UserPasswordUpdateSerializer for update user password to new password
            user_serializer = UserPasswordUpdateSerializer(instance=otp_details.user, data=request.data)

            # Checking for data validity
            if user_serializer.is_valid():
                # Updating actual recode
                user_serializer.update(instance=otp_details.user, validated_data=request.data)

                response_data["success"] = True
                response_data["message"] = "User password successfully changed"
                response_data["data"] = email
                return Response(data=response_data, status=200)

            else:
                response_data["success"] = False
                response_data["message"] = "Data missing or invalid"
                response_data["data"] = user_serializer.errors
                return Response(data=response_data, status=400)

        # If OTP ID is invalid user is unable to change password. So returning error response
        except OtpDetails.DoesNotExist:
            response_data["success"] = False
            response_data["message"] = "Invalid OTP ID"
            response_data["data"] = None
            return Response(data=response_data, status=401)

    # If unexpected error occurs while performing this task, Handling it and returning server error
    except Exception as e:
        print(traceback.format_exc())
        response_data["success"] = False
        response_data["message"] = "Unexpected error"
        response_data["data"] = str(e)
        return Response(data=response_data, status=500)
