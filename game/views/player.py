from rest_framework.decorators import api_view
from rest_framework.response import Response

from game.models import Player, PlayerRoundScore
from authentication.decorators import admin, coach_and_admin
from game.serializers import PlayerSerializer

import numpy as np
import traceback


@api_view(["GET"])
@admin()
def get_all(request):
    try:
        players = Player.objects.all()
        serializer = PlayerSerializer(instance=players, many=True)
        return Response(data={"success": True, "message": "Players successfully fetched", "data": serializer.data},
                        status=200)
    except Exception:
        return Response(data={"success": False, "message": "Unexpected error", "data": None}, status=500)


@api_view(["GET"])
@coach_and_admin()
def get_by_team(request, team_id):
    try:
        players = Player.objects.filter(team_id=team_id)
        serializer = PlayerSerializer(instance=players, many=True)
        return Response(data={"success": True, "message": "Players successfully fetched", "data": serializer.data},
                        status=200)
    except Exception:
        return Response(data={"success": False, "message": "Unexpected error", "data": None}, status=500)


@api_view(["GET"])
@admin()
def get_by_game(request, game_id):
    try:
        players = Player.objects.filter(round__game_id=game_id)
        serializer = PlayerSerializer(instance=players, many=True)
        return Response(data={"success": True, "message": "Players successfully fetched", "data": serializer.data},
                        status=200)
    except Exception as e:
        print(traceback.format_exc())
        return Response(data={"success": False, "message": "Unexpected error", "data": None}, status=500)


@api_view(["GET"])
@coach_and_admin()
def get_by_percentile(request, team_id, percentile):
    try:
        # Getting all players average score by using custom query set
        players_score = PlayerRoundScore.objects.get_players_average_in_team(team_id=team_id)

        if players_score.count() != 0:
            # Populate those average marks into the numpy array using list comprehensive
            avg_score_array = np.array([player_score['avg_score'] for player_score in list(players_score)])

            # Calculate percentile value by using help of numpy
            percentile_value = np.percentile(avg_score_array, int(percentile))

            # Getting players who's average is in 90th percentile and getting those players data using 'in'
            players = Player.objects.filter(
                id__in=players_score.filter(avg_score__gte=percentile_value).values_list('player_id'))

            serializer = PlayerSerializer(instance=players, many=True)
            return Response(data={"success": True, "message": "Players successfully fetched", "data": serializer.data},
                            status=200)

        else:
            return Response(data={"success": True, "message": "Players successfully fetched", "data": list()},
                            status=200)

    except Exception as e:
        return Response(data={"success": False, "message": "Unexpected error", "data": None}, status=500)


@api_view(["GET"])
@coach_and_admin()
def get_by_player_id(request, player_id):
    try:
        player = Player.objects.get(id=player_id)
        serializer = PlayerSerializer(instance=player)
        return Response(data={"success": True, "message": "Players successfully fetched", "data": serializer.data},
                        status=200)
    except Exception:
        print(traceback.format_exc())
        return Response(data={"success": False, "message": "Unexpected error", "data": None}, status=500)
