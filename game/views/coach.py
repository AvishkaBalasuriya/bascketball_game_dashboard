from rest_framework.decorators import api_view
from rest_framework.response import Response

from game.models import Coach
from authentication.decorators import admin
from game.serializers import CoachSerializer

import traceback


@api_view(["GET"])
@admin()
def get_all(request):
    try:
        coaches = Coach.objects.all()
        serialized_data = CoachSerializer(instance=coaches, many=True)
        return Response(data={"success": True, "message": "Coaches successfully fetched", "data": serialized_data.data},
                        status=200)
    except Exception:
        return Response(data={"success": False, "message": "Unexpected error", "data": None}, status=500)


@api_view(["GET"])
@admin()
def get_by_player(request, player_id):
    try:
        coach = Coach.objects.select_related('team').filter(team__player__id=player_id)
        serialized_data = CoachSerializer(instance=coach, many=True)
        return Response(data={"success": True, "message": "Coaches successfully fetched", "data": serialized_data.data},
                        status=200)
    except Exception:
        return Response(data={"success": False, "message": "Unexpected error", "data": None}, status=500)


@api_view(["GET"])
@admin()
def get_by_team(request, team_id):
    try:
        coach = Coach.objects.filter(team__id=team_id)
        serialized_data = CoachSerializer(instance=coach, many=True)
        return Response(data={"success": True, "message": "Coaches successfully fetched", "data": serialized_data.data},
                        status=200)
    except Exception as e:
        return Response(data={"success": False, "message": "Unexpected error", "data": None}, status=500)
