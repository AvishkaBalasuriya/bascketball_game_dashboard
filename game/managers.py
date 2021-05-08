from django.db.models import Manager

from .query_sets import TeamRoundScoreQuerySet, PlayerRoundScoreQuerySet, RoundQuerySet


class PlayerRoundScoreManager(Manager):
    def get_query_set(self):
        return PlayerRoundScoreQuerySet(self.model, using=self._db)

    def get_player_average(self, player_id):
        return self.get_query_set().get_player_average(player_id=player_id)

    def get_players_average_in_team(self, team_id):
        return self.get_query_set().get_players_average_in_team(team_id=team_id)


class TeamRoundScoreManager(Manager):
    def get_query_set(self):
        return TeamRoundScoreQuerySet(self.model, using=self._db)

    def get_team_average(self, team_id):
        return self.get_query_set().get_team_average(team_id=team_id)

    def get_teams_average(self):
        return self.get_query_set().get_teams_average()


class RoundManager(Manager):
    def get_query_set(self):
        return RoundQuerySet(self.model, using=self._db)

    def get_games_played(self, player_id):
        return self.get_query_set().get_games_played(player_id=player_id)

    def get_team_score(self, game_id, team_id):
        return self.get_query_set().get_team_score(game_id=game_id, team_id=team_id)
