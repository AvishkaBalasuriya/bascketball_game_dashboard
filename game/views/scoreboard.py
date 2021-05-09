from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from game.models import Tournament, Game, PlayerRoundScore
from game.serializers import TournamentSerializer, GameSerializer, PlayerRoundScoreSerializer

import traceback


@api_view(["GET"])
@permission_classes([AllowAny])
def get_all(request):
    try:
        tournaments = Tournament.objects.all()
        serializer = TournamentSerializer(instance=tournaments, many=True)

        return Response(data={"success": True, "message": "Teams successfully fetched", "data": serializer.data},
                        status=200)
    except Exception:
        return Response(data={"success": False, "message": "Unexpected error", "data": None}, status=500)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_by_tournament_id(request, tournament_id):
    try:
        try:
            tournament = Tournament.objects.get(id=tournament_id)
            serializer = TournamentSerializer(instance=tournament, many=False)
            return Response(
                data={"success": True, "message": "All tournament data successfully fetched", "data": serializer.data},
                status=200)
        except Tournament.DoesNotExist:
            return Response(
                data={"success": True, "message": "No tournament data", "data": None},
                status=200)
    except Exception:
        return Response(data={"success": False, "message": "Unexpected error", "data": None}, status=500)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_all_games_by_tournament(request, tournament_id):
    try:
        games = Game.objects.filter(stage__tournament_id=tournament_id)
        serializer = GameSerializer(instance=games, many=True)
        return Response(
            data={"success": True, "message": "All tournament data successfully fetched", "data": serializer.data},
            status=200)
    except Exception as e:
        return Response(data={"success": False, "message": "Unexpected error", "data": None}, status=500)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_score_by_round(request, game_id):
    try:
        game_rounds = PlayerRoundScore.objects.filter(round__game_id=game_id)
        serializer = PlayerRoundScoreSerializer(instance=game_rounds, many=True)
        return Response(
            data={"success": True, "message": "All tournament data successfully fetched", "data": serializer.data},
            status=200)
    except Exception as e:
        return Response(data={"success": False, "message": "Unexpected error", "data": None}, status=500)
