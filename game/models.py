from django.db import models

from .managers import PlayerRoundScoreManager, TeamRoundScoreManager, RoundManager


class Team(models.Model):
    name = models.CharField(max_length=100)


class Coach(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    country = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)


class Player(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    country = models.CharField(max_length=100)
    height = models.DecimalField(decimal_places=2, max_digits=5)
    weight = models.DecimalField(decimal_places=2, max_digits=5)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    @property
    def games_played(self):
        return Round.objects.get_games_played(player_id=self.id)

    @property
    def average_score(self):
        average_score = PlayerRoundScore.objects.get_player_average(player_id=self.id).values('avg_score')
        return average_score.first()[
            'avg_score'] if average_score.count() != 0 else 0

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    class Meta:
        managed = True


class Tournament(models.Model):
    name = models.CharField(max_length=100)
    venue = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    teams = models.ManyToManyField(Team)
    winner = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="champion_team")


class Stage(models.Model):
    STAGES = [(0, "Qualifying Stage"), (1, "Quarter Finals"), (2, "Semi Finals"), (3, "Final")]

    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, choices=STAGES)
    start_date = models.DateField()
    end_date = models.DateField()


class Game(models.Model):
    teams = models.ManyToManyField(Team, related_name='participated_teams')
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    winner = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='winning_team')
    looser = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='loose_team')
    is_draw = models.BooleanField(default=False)
    host_date = models.DateField()

    @property
    def winning_team_total_score(self):
        return \
            Round.objects.get_team_score(game_id=self.id, team_id=self.winner.id)[0]['total']

    @property
    def loose_team_total_score(self):
        return \
            Round.objects.get_team_score(game_id=self.id, team_id=self.looser.id)[0]['total']


class Round(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    players = models.ManyToManyField(Player)
    round_number = models.IntegerField()

    objects = RoundManager()


class PlayerRoundScore(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    score = models.IntegerField()

    objects = PlayerRoundScoreManager()


class TeamRoundScore(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    score = models.IntegerField()

    objects = TeamRoundScoreManager()
