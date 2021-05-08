from rest_framework.serializers import ModelSerializer, ReadOnlyField

from .models import Player, Coach, Tournament, Team, Game, Stage, PlayerRoundScore, Round


class PlayerSerializer(ModelSerializer):
    class Meta(object):
        model = Player
        fields = (
            'id', 'first_name', 'last_name', 'date_of_birth', 'country', 'height', 'weight', 'team', 'games_played',
            'average_score')


class CoachSerializer(ModelSerializer):
    class Meta(object):
        model = Coach
        fields = ('id', 'first_name', 'last_name', 'country', 'date_of_birth', 'team',)


class CoachByPlayer(ModelSerializer):
    player = PlayerSerializer
    coach = CoachSerializer

    class Meta(object):
        model = Player
        fields = ()


class TeamSerializer(ModelSerializer):
    class Meta(object):
        model = Team
        fields = ('id', 'name',)


class TournamentSerializer(ModelSerializer):
    participated_teams = TeamSerializer(source='teams', many=True)
    winning_team = TeamSerializer(source='winner', many=False)

    class Meta(object):
        model = Tournament
        fields = ('id', 'name', 'venue', 'start_date', 'end_date', 'participated_teams', 'winning_team',)


class StageSerializer(ModelSerializer):
    class Meta(object):
        model = Stage
        fields = ('id', 'tournament', 'name', 'start_date', 'end_date',)


class GameRoundSerializer(ModelSerializer):
    class Meta(object):
        model = Round()
        fields = ('round_number',)


class PlayerRoundScoreSerializer(ModelSerializer):
    game_round = ReadOnlyField(source='round.round_number')
    played_player_id = ReadOnlyField(source='player.id')
    played_player_team = ReadOnlyField(source='player.team.id')

    class Meta(object):
        model = PlayerRoundScore
        fields = ('game_round', 'played_player_id', 'played_player_team', 'score',)


class GameSerializer(ModelSerializer):
    participated_teams = TeamSerializer(source='teams', many=True)
    game_stage = StageSerializer(source='stage', many=False)
    winning_team = TeamSerializer(source='winner', many=False)
    loose_team = TeamSerializer(source='looser', many=False)

    class Meta(object):
        model = Game
        fields = ('id', 'game_stage', 'participated_teams', 'winning_team', 'loose_team', 'host_date',
                  'winning_team_total_score', 'loose_team_total_score',)
