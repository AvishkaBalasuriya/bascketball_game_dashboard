from rest_framework.decorators import api_view
from rest_framework.response import Response

from game.models import Team
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
    except Exception as e:
        print(e)
        return Response(data={"success": False, "message": "Unexpected error", "data": None}, status=500)


@api_view(["GET"])
@coach_and_admin()
def get_team_average(request, team_id):
    try:
        try:
            team = Team.objects.get(id=team_id)

            serializer = TeamSerializer(instance=team, many=False)

            return Response(data={"success": True, "message": "Team successfully fetched", "data": serializer.data},
                            status=200)
        except Team.DoesNotExist:
            return Response(data={"success": True, "message": "No team", "data": None},
                            status=200)
    except Exception as e:
        return Response(data={"success": False, "message": "Unexpected error", "data": None}, status=500)
