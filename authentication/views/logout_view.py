from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import logout

from rest_framework.decorators import api_view
from rest_framework.response import Response


# This view is to user logout
# This is a POST method API and needed data is taken by django session internally
# This endpoint is allow to anyone
@api_view(["POST"])
@ensure_csrf_cookie
def user_logout(request):
    response_data = {}
    try:

        # Removing user session
        logout(request)

        response_data["success"] = True
        response_data["message"] = "User successfully logged out"
        response_data["data"] = None
        return Response(data=response_data, status=200)

    except Exception as e:

        response_data["success"] = False
        response_data["message"] = "Unexpected error"
        response_data["data"] = str(e)
        return Response(data=response_data, status=500)
