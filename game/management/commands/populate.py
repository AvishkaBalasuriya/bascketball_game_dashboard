from django.core.management.base import BaseCommand
from django.db import transaction

from faker import Faker
from wasabi import msg

from game.models import Coach, Team, Player, Tournament, Stage, Game, Round, PlayerRoundScore, TeamRoundScore

import random
import decimal
import uuid


class Command(BaseCommand):
    def populate_coaches(self, faker: Faker):
        teams = Team.objects.all()
        for team in teams:
            coach = Coach(id=str(uuid.uuid4()), first_name=faker.first_name(), last_name=faker.last_name(),
                          date_of_birth=faker.date(),
                          country=faker.country(), team=team)
            coach.save()
        msg.good("Coaches data successfully populated")

    def populate_teams(self, faker: Faker):
        for i in range(16):
            team = Team(name=faker.name())
            team.save()
        msg.good("Teams data successfully populated")

    def populate_players(self, faker: Faker):
        teams = Team.objects.all()
        for team in teams:
            for i in range(10):
                player = Player(id=str(uuid.uuid4()),
                                first_name=faker.first_name(),
                                last_name=faker.last_name(),
                                date_of_birth=faker.date(),
                                country=faker.country(),
                                height=round(decimal.Decimal(random.randrange(20000)) / 100, 2),
                                weight=round(decimal.Decimal(random.randrange(20000)) / 100, 2),
                                team=team)
                player.save()
        msg.good("Players data successfully populated")

    def populate_tournaments(self, faker: Faker):
        teams = Team.objects.all()
        for i in range(5):
            tournament = Tournament(name=faker.name(), venue=faker.country(), start_date=faker.date(),
                                    end_date=faker.date(), winner=random.choice(teams))
            tournament.save()
            tournament.teams.set(teams)
        msg.good("Tournament data successfully populated")

    def populate_stages(self, faker: Faker):
        stage_list = [0, 1, 2, 3]
        tournaments = Tournament.objects.all()
        for tournament in tournaments:
            for i in range(0, 4):
                stage = Stage(tournament=tournament, name=stage_list[i], start_date=faker.date(),
                              end_date=faker.date())
                stage.save()
        msg.good("Game stage data successfully populated")

    def populate_games(self, faker: Faker):
        quarter_final_round_teams = []
        semi_final_round_teams = []
        final_round_teams = []

        teams = Team.objects.all()
        stages = Stage.objects.all().order_by('tournament_id')

        qualify_round_teams = teams

        for stage in stages:
            if stage.name == "0":
                for i in range(0, 16, 2):
                    winning_team = self._add_game(qualify_round_teams, stage, i, faker)
                    quarter_final_round_teams.append(winning_team[0])
            if stage.name == "1":
                for i in range(0, 8, 2):
                    winning_team = self._add_game(quarter_final_round_teams, stage, i, faker)
                    semi_final_round_teams.append(winning_team[0])

            if stage.name == "2":
                for i in range(0, 4, 2):
                    winning_team = self._add_game(semi_final_round_teams, stage, i, faker)
                    final_round_teams.append(winning_team[0])

            if stage.name == "3":
                for i in range(0, 2, 2):
                    winning_team = self._add_game(final_round_teams, stage, i, faker)
                    stage.tournament.winner = winning_team[0]
                    stage.save()
        msg.good("Game data successfully populated")

    def _add_game(self, team_arr, stage, i, faker):
        game_teams = [team_arr[i], team_arr[i + 1]]
        winning_team = [random.choice(game_teams)]
        loose_team = list(set(game_teams).symmetric_difference(set(winning_team)))[0]
        game = Game(winner=winning_team[0], stage=stage, host_date=faker.date(), looser=loose_team)
        game.save()
        game.teams.set(game_teams)
        return winning_team

    def _populate_rounds(self, game, winning_team_players, loose_team_players, winning_team_score, loose_team_score,
                         winning_team_id):
        winning_team_round_score = self._split_a_total(winning_team_score, 4, [i for i in range(1, 5)])
        loose_team_round_score = self._split_a_total(loose_team_score, 4, [i for i in range(1, 5)])
        for i in range(1, 5):
            game_players = winning_team_players + loose_team_players
            round = Round(game=game, round_number=i)
            round.save()
            round.players.set(game_players)

            self._populate_player_round_score(round, game_players, winning_team_round_score[i],
                                              loose_team_round_score[i], winning_team_players, loose_team_players,
                                              winning_team_id)
            self._populate_team_round_scores(round, game.teams)

    def _populate_team_round_scores(self, round, game_teams):
        for team in game_teams.all():
            players = PlayerRoundScore.objects.filter(round=round, player__team_id=team.id)
            teams_score = 0
            for player in players:
                teams_score += player.score
            team_round_score = TeamRoundScore(round=round, team=team, score=teams_score)
            team_round_score.save()

    def _populate_player_round_score(self, round, game_players, winning_team_score, loose_team_score,
                                     winning_team_players, loose_team_players, winning_team_id):
        winning_team_divided_score = self._split_a_total(winning_team_score, len(winning_team_players),
                                                         winning_team_players)
        loose_team_divided_score = self._split_a_total(loose_team_score, len(loose_team_players),
                                                       loose_team_players)

        for player in game_players:
            if player.team.id == winning_team_id:
                score = winning_team_divided_score[player.id]
            else:
                score = loose_team_divided_score[player.id]
            player = PlayerRoundScore(round=round, player=player, score=score)
            player.save()

    def _split_a_total(self, total, n, key_list):
        splitted_total = {}
        total_up_to_now = 0
        for i in range(0, n):
            try:
                identifier = key_list[i].id
            except AttributeError:
                identifier = key_list[i]

            if i == 0:
                value = round(total / n)
                splitted_total[identifier] = value
            elif i == n - 1:
                value = total - total_up_to_now
                splitted_total[identifier] = value
            else:
                try:
                    value = random.randint(0, (total - total_up_to_now) - 1)
                except ValueError:
                    value = 0
                splitted_total[identifier] = value

            total_up_to_now += value
        return splitted_total

    def populate_game_scores(self):
        games = Game.objects.all()
        for game in games:
            winning_team_score = random.randint(4, 20)
            loose_team_score = random.randint(0, winning_team_score - 1)

            winning_team_players = random.sample(list(Player.objects.filter(team_id=game.winner.id)), 5)
            loose_team_players = random.sample(list(Player.objects.filter(team_id=game.looser.id)), 5)

            self._populate_rounds(game, winning_team_players, loose_team_players, winning_team_score, loose_team_score,
                                  game.winner.id)
        msg.good("All game scores successfully divided among players")

    def handle(self, *args, **options):
        fake = Faker()
        Coach.objects.all().delete()
        Team.objects.all().delete()
        Player.objects.all().delete()
        Tournament.objects.all().delete()
        Stage.objects.all().delete()
        Game.objects.all().delete()
        Round.objects.all().delete()
        PlayerRoundScore.objects.all().delete()
        TeamRoundScore.objects.all().delete()
        with transaction.atomic():
            self.populate_teams(fake)
            self.populate_coaches(fake)
            self.populate_players(fake)
            self.populate_tournaments(fake)
            self.populate_stages(fake)
            self.populate_games(fake)
            self.populate_game_scores()

        msg.good("All fake data populated")
