from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from authentication.models import User, OtpDetails
from authentication.serializers import OTPCreateSerializer

import traceback


# This view is use to send an OTP code to the user email
# This is a POST method API and it required email in request data
# This endpoint is allow to anyone
@api_view(["POST"])
@permission_classes([AllowAny])
def send_otp(request):
    response_data = {}
    try:
        user_email = request.data["user"]
        try:
            # Getting user instance by email
            user = User.objects.get(email=user_email)

            # Creating serializer with data
            otp_create_serializer = OTPCreateSerializer(data=request.data, context={"user": user})

            # Checking for validity
            if otp_create_serializer.is_valid():

                # Saving OTP details
                result = otp_create_serializer.save()

                if result:
                    response_data["success"] = True
                    response_data["message"] = "OTP successfully sent"
                    response_data["data"] = None
                    return Response(data=response_data, status=200)

                elif result == False:
                    response_data["success"] = False
                    response_data["message"] = "Unable to send email"
                    response_data["data"] = None
                    return Response(data=response_data, status=424)

                else:
                    response_data["success"] = False
                    response_data["message"] = "There is already an active OTP for user. Try again in two minutes"
                    response_data["data"] = None
                    return Response(data=response_data, status=200)

            else:
                response_data["success"] = False
                response_data["message"] = "Data missing or invalid"
                response_data["data"] = otp_create_serializer.errors

                return Response(data=response_data, status=400)

        # If user request with invalid user email, Handling it and sending error response
        except User.DoesNotExist:

            response_data["success"] = False
            response_data["message"] = "An account with provided email not exists"
            response_data["data"] = None

            return Response(data=response_data, status=400)

    # If unexpected error occurs while performing this task, Handling it and returning server error
    except Exception as e:
        response_data["success"] = False
        response_data["message"] = "Unexpected error"
        response_data["data"] = str(e)
        return Response(data=response_data, status=500)


# This view is use to verify an OTP code
# This is a POST method API and it required email and otp_code in request data
# This endpoint is allow to anyone
@api_view(["POST"])
@permission_classes([AllowAny])
def verify_otp(request):
    response_data = {}
    try:
        email = request.data["email"]
        otp = request.data["otp_code"]

        try:
            # Getting OTP details by user email and OTP code
            otp_details = OtpDetails.objects.get_data_by_email(email=email, otp=otp)

            # Checking for OTP expiration
            if otp_details.is_expired:

                response_data["success"] = False
                response_data["message"] = "OTP is expired"
                response_data["data"] = None
                return Response(data=response_data, status=498)

            else:
                # Changing is_active attribute to False. So This OTP code is no longer available
                otp_details.is_active = False
                otp_details.save()

                response_data["success"] = True
                response_data["message"] = "OTP code successfully verified"
                response_data["data"] = otp_details.id

                return Response(data=response_data, status=200)

        except OtpDetails.DoesNotExist:
            response_data["success"] = False
            response_data["message"] = "Invalid OTP or Email"
            response_data["data"] = None
            return Response(data=response_data, status=401)

    # If unexpected error occurs while performing this task, Handling it and returning server error
    except Exception as e:
        response_data["success"] = False
        response_data["message"] = "Unexpected error"
        response_data["data"] = str(e)
        return Response(data=response_data, status=500)
