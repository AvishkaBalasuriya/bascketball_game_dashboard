from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from authentication.models import User, OtpDetails
from game.models import Coach, Player, Team

from faker import Faker
import uuid


class GameTest(TestCase):
    def setUp(self):
        self._client = Client()
        self._faker = Faker()

        self._test_email = "test@gmail.com"
        self._test_password = "myPassword"
        self._test_first_name = "First Name Test"
        self._test_last_name = "Last Name Test"
        self._test_country = "Sri Lanka"
        self._test_otp = 123456

        self._get_all_players = reverse('get_all_players')
        # self._get_players_by_team = reverse('get_players_by_team', args=(1,))
        # self._get_players_by_percentile = reverse('get_players_by_percentile', args=["team_id"])
        # self._get_players_by_game = reverse('get_players_by_game', args=["game_id"])
        # self._get_player_by_player_id = reverse('get_player_by_player_id', args=["player_id"])
        #
        # self._get_all_coaches = reverse('get_all_coaches')
        # self._get_coaches_by_player = reverse('get_coaches_by_player', args=["player_id"])
        # self._get_coaches_by_team = reverse('get_coaches_by_team', args=["team_id"])
        #
        # self._get_all_teams = reverse('get_all_teams')
        # self._get_team_average = reverse('get_team_average', args=["team_id"])
        # self._get_teams_average = reverse('get_teams_average')
        #
        # self._get_scoreboard = reverse('get_all_scoreboard')
        # self._get_scoreboard_by_tournament_id = reverse('get_scoreboard_by_tournament_id', args=["tournament_id"])
        # self._get_all_games_by_tournament = reverse('get_all_games_by_tournament', args=["tournament_id"])
        # self._get_game_score_by_round = reverse('get_game_score_by_round', args=["game_id"])

    def create_user_account(self, is_admin=False, coach=None, player=None):
        user = User.objects.create(email=self._test_email, first_name=self._test_first_name,
                                   last_name=self._test_last_name, is_admin=is_admin,
                                   coach=coach, player=player)
        user.set_password(self._test_password)
        user.save()
        return user

    def create_player(self):
        team = self.create_team()
        player = Player.objects.create(id=str(uuid.uuid4()), first_name=self._test_first_name,
                                       last_name=self._test_last_name, country=self._test_country,
                                       date_of_birth=timezone.now(), height=189.93, weight=80.34, team=team)
        return player

    def create_coach(self):
        team = self.create_team()
        coach = Coach.objects.create(id=str(uuid.uuid4()), first_name=self._test_first_name,
                                     last_name=self._test_last_name, country=self._test_country,
                                     date_of_birth=timezone.now(), team=team)
        return coach

    def create_otp(self, user, time_delta=2):
        otp = OtpDetails.objects.create(id=str(uuid.uuid4()), user=user, otp_code=self._test_otp, is_active=True,
                                        expire_date=timezone.now() + timedelta(minutes=time_delta))
        return otp

    def create_team(self):
        return Team.objects.create(name="test_team")

    def log_user(self, email, password):
        self._client.login(email=email, password=password)

    def test_get_all_players_without_login(self):
        response = self._client.get(self._get_all_players)

        self.assertEqual(response.status_code, 403)

    def test_get_all_players_when_empty(self):
        self.create_user_account(is_admin=True)
        self.log_user(self._test_email, self._test_password)

        response = self._client.get(self._get_all_players)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["success"], True)
        self.assertEqual(len(response.data["data"]), 0)

    def test_get_all_players_when_there_is_data(self):
        self.create_user_account(is_admin=True)
        self.log_user(self._test_email, self._test_password)

        self.create_player()

        response = self._client.get(self._get_all_players)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["success"], True)
        self.assertNotEqual(len(response.data["data"]), 0)

    def test_get_all_players_with_invalid_user_type(self):
        self.create_user_account(player=self.create_player())
        self.log_user(self._test_email, self._test_password)

        self.create_player()

        response = self._client.get(self._get_all_players)

        self.assertEqual(response.status_code, 403)

    def test_get_all_players_by_team(self):
        url = reverse('get_players_by_team', args=(1,))

        self.create_user_account(is_admin=True)
        self.log_user(self._test_email, self._test_password)

        self.create_player()

        response = self._client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["success"], True)

    def test_get_all_players_by_percentile(self):
        url = reverse('get_players_by_percentile', args=(1, 90,))

        self.create_user_account(is_admin=True)
        self.log_user(self._test_email, self._test_password)

        self.create_player()

        response = self._client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["success"], True)

    def test_get_all_players_by_game(self):
        url = reverse('get_players_by_game', args=(1,))

        self.create_user_account(is_admin=True)
        self.log_user(self._test_email, self._test_password)

        self.create_player()

        response = self._client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["success"], True)

    def test_get_all_players_by_id(self):
        player = self.create_player()

        url = reverse('get_player_by_player_id', args=(player.id,))

        self.create_user_account(is_admin=True)
        self.log_user(self._test_email, self._test_password)

        response = self._client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["success"], True)

    def test_get_all_coaches(self):
        url = reverse('get_all_coaches')

        self.create_user_account(is_admin=True)
        self.log_user(self._test_email, self._test_password)

        self.create_coach()

        response = self._client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["success"], True)

    def test_get_coaches_by_player(self):
        url = reverse('get_coaches_by_player', args=(1,))

        self.create_user_account(is_admin=True)
        self.log_user(self._test_email, self._test_password)

        self.create_player()
        self.create_coach()

        response = self._client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["success"], True)

    def test_get_coaches_by_team(self):
        url = reverse('get_coaches_by_team', args=(1,))

        self.create_user_account(is_admin=True)
        self.log_user(self._test_email, self._test_password)

        self.create_player()
        self.create_coach()
        self.create_team()

        response = self._client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["success"], True)

    def test_get_all_team(self):
        url = reverse('get_all_teams')

        self.create_user_account(is_admin=True)
        self.log_user(self._test_email, self._test_password)

        self.create_player()
        self.create_coach()
        self.create_team()

        response = self._client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["success"], True)

    def test_get_all_team_average(self):
        team_id = self.create_team().id
        url = reverse('get_team_average', args=(team_id,))

        self.create_user_account(is_admin=True)
        self.log_user(self._test_email, self._test_password)

        self.create_player()
        self.create_coach()

        response = self._client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["success"], True)

    def test_get_all_scoreboards(self):
        url = reverse('get_all_scoreboard')

        self.create_user_account(is_admin=True)
        self.log_user(self._test_email, self._test_password)

        self.create_player()
        self.create_coach()
        self.create_team()

        response = self._client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["success"], True)

    def test_get_scoreboards_by_tournament(self):
        url = reverse('get_scoreboard_by_tournament_id', args=(1,))

        self.create_user_account(is_admin=True)
        self.log_user(self._test_email, self._test_password)

        self.create_player()
        self.create_coach()
        self.create_team()

        response = self._client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["success"], True)

    def test_get_scoreboards_for_game_by_tournament(self):
        url = reverse('get_all_games_by_tournament', args=(1,))

        self.create_user_account(is_admin=True)
        self.log_user(self._test_email, self._test_password)

        self.create_player()
        self.create_coach()
        self.create_team()

        response = self._client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["success"], True)

    def test_get_scoreboards_for_game_by_game_id(self):
        url = reverse('get_game_score_by_round', args=(1,))

        self.create_user_account(is_admin=True)
        self.log_user(self._test_email, self._test_password)

        self.create_player()
        self.create_coach()
        self.create_team()

        response = self._client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["success"], True)
