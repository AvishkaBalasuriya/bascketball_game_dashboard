from rest_framework.decorators import api_view
from rest_framework.response import Response

from game.models import Team, TeamRoundScore
from authentication.decorators import admin, coach_and_admin
from game.serializers import TeamSerializer


@api_view(["GET"])
@admin()
def get_all(request):
    try:
        teams = Team.objects.all()
        serializer = TeamSerializer(instance=teams, many=True)
        return Response(data={"success": True, "message": "Teams successfully fetched", "data": serializer.data},
                        status=200)
    except Exception:
        return Response(data={"success": False, "message": "Unexpected error", "data": None}, status=500)


@api_view(["GET"])
@coach_and_admin()
def get_team_average(request, team_id):
    try:
        teams = TeamRoundScore.objects.get_team_average(team_id)
        serializer = TeamSerializer(instance=teams, many=False)
        return Response(data={"success": True, "message": "Team successfully fetched", "data": serializer.data},
                        status=200)
    except Exception:
        return Response(data={"success": False, "message": "Unexpected error", "data": None}, status=500)


@api_view(["GET"])
@admin()
def get_teams_average(request):
    try:
        teams = TeamRoundScore.objects.get_teams_average()
        serializer = TeamSerializer(instance=teams, many=True)
        return Response(data={"success": True, "message": "Teams successfully fetched", "data": serializer.data},
                        status=200)
    except Exception:
        return Response(data={"success": False, "message": "Unexpected error", "data": None}, status=500)
