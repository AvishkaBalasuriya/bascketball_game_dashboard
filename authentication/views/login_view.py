from django.contrib.auth import authenticate, login

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

import traceback


# This view is to user login
# This is a POST method API and it required email,password as it's request data
# This endpoint is allow to anyone
@api_view(["POST"])
@permission_classes([AllowAny])
def user_login(request):
    response_data = {}
    try:
        # Calling custom authentication backend via django authentication
        user = authenticate(request)

        # Checking if user is authenticated or not
        if user:

            # login user with django session authentication
            login(request, user=user)

            response_data["success"] = True
            response_data["message"] = "User successfully logged in to system"
            response_data["data"] = user.email

            return Response(data=response_data, status=200)

        # Handling user credentials invalid scenario
        else:

            response_data["success"] = False
            response_data["message"] = "Email or password is incorrect"
            response_data["data"] = None
            return Response(data=response_data, status=401)

    except Exception as e:
        response_data["success"] = False
        response_data["message"] = "Unexpected error"
        response_data["data"] = str(e)
        return Response(data=response_data, status=500)
