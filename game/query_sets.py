from django.db.models import QuerySet, Avg, Count, Sum


class TeamRoundScoreQuerySet(QuerySet):
    def get_teams_average(self):
        return self.values('team_id').annotate(
            avg_score=Avg('score'))

    def get_team_average(self, team_id):
        return self.filter(team__id=team_id).values('team_id').annotate(
            avg_score=Avg('score'))


class PlayerRoundScoreQuerySet(QuerySet):
    def get_players_average(self):
        return self.values('player_id').annotate(
            avg_score=Avg('score'))

    def get_player_average(self, player_id):
        return self.filter(player__id=player_id).values('player_id').annotate(
            avg_score=Avg('score'))

    def get_players_average_in_team(self, team_id):
        return self.filter(player__team_id=team_id).values('player_id').annotate(
            avg_score=Avg('score'))


class RoundQuerySet(QuerySet):
    def get_games_played(self, player_id):
        return self.filter(players__id=player_id).values('game_id').annotate(Count('game_id', distinct=True)).count()

    def get_team_score(self, game_id, team_id):
        return self.filter(game__id=game_id, teamroundscore__team_id=team_id).values('game').annotate(
            total=Sum('teamroundscore__score')).values('total')
