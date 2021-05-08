from rest_framework.decorators import api_view
from rest_framework.response import Response

from authentication.serializers import UserStatSerializer
from authentication.models import UserStat
from authentication.decorators import admin

import traceback

# This view is to get user statistics
# This is a GET method API and this is only available for the admins
@api_view(["GET"])
@admin()
def get_stat(request):
    response_data = {}
    try:
        # Getting all user stats and serializing them
        user_stats = UserStat.objects.all()
        serializer = UserStatSerializer(instance=user_stats, many=True)

        response_data["success"] = True
        response_data["message"] = "User Statistics successfully fetched"
        response_data["data"] = serializer.data
        return Response(data=response_data, status=200)

    except Exception as e:
        response_data["success"] = False
        response_data["message"] = "Unexpected error"
        response_data["data"] = str(e)
        return Response(data=response_data, status=500)
