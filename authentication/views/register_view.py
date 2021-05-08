from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from authentication.serializers import UserCreateSerializer
from authentication.decorators import admin


# This view is to user registration
# This is a POST method API and this is only available for the admins. Other users can't use this. I assume that league
# admins are responsible for giving access to the system.
# This endpoint is allow to anyone
@api_view(["POST"])
@admin()
def user_register(request):
    response_data = {}
    try:

        # Initializing user create serializer
        user_create_serializer = UserCreateSerializer(data=request.data, context={"request": request.data})

        # Checking for serializer validity. I override default validate method so I can handle scenarios like, Duplicate
        # accounts etc.
        if user_create_serializer.is_valid():

            # Saving user with custom save function
            user = user_create_serializer.save()

            response_data["success"] = True
            response_data["message"] = "User successfully created"
            response_data["data"] = user.email
            return Response(data=response_data, status=200)

        else:
            response_data["success"] = False
            response_data["message"] = "Missing fields or invalid data"
            response_data["data"] = user_create_serializer.errors
            return Response(data=response_data, status=400)

    except Exception as e:
        response_data["success"] = False
        response_data["message"] = "Unexpected error"
        response_data["data"] = str(e)
        return Response(data=response_data, status=500)
