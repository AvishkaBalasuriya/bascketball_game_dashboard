from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from authentication.models import User, OtpDetails, UserStat
from game.models import Coach, Player, Team

from faker import Faker
import uuid


class AuthenticationTest(TestCase):
    def setUp(self):
        self._client = Client()
        self._faker = Faker()

        self._test_email = "test@gmail.com"
        self._test_password = "myPassword"
        self._test_first_name = "First Name Test"
        self._test_last_name = "Last Name Test"
        self._test_country = "Sri Lanka"
        self._test_otp = 123456

        self._login_url = reverse('login')
        self._register_url = reverse('register')
        self._logout_url = reverse('logout')
        self._send_otp = reverse('send_otp')
        self._verify_otp = reverse('verify_otp')
        self._forget_password = reverse('forget_password')
        self._user_stat = reverse('user_stat')

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

    def test_login_with_invalid_credentials(self):
        response = self._client.post(self._login_url, data={
            "email": self._test_email,
            "password": self._test_password
        })

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["success"], False)

    def test_login_with_valid_credentials_admin(self):
        self.create_user_account(is_admin=True)

        response = self._client.post(self._login_url, data={
            "email": self._test_email,
            "password": self._test_password
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["success"], True)

    def test_login_with_valid_credentials_coach(self):
        self.create_user_account(coach=self.create_coach())

        response = self._client.post(self._login_url, data={
            "email": self._test_email,
            "password": self._test_password
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["success"], True)

    def test_login_with_valid_credentials_player(self):
        self.create_user_account(player=self.create_player())

        response = self._client.post(self._login_url, data={
            "email": self._test_email,
            "password": self._test_password
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["success"], True)

    def test_register_without_login_to_account(self):
        response = self._client.post(self._register_url, data={
            "email": self._test_email,
            "password": self._test_password
        })

        self.assertEqual(response.status_code, 403)

    def test_register_with_login_to_coach_account(self):
        self.create_user_account(coach=self.create_coach())

        response = self._client.post(self._register_url, data={
            "email": self._test_email,
            "password": self._test_password
        })

        self.assertEqual(response.status_code, 403)

    def test_register_with_login_to_admin_account(self):
        self.create_user_account(is_admin=True)
        self.log_user(email=self._test_email, password=self._test_password)

        response = self._client.post(self._register_url, data={
            "email": self._faker.email(),
            "password": self._faker.password(),
            "first_name": self._faker.first_name(),
            "last_name": self._faker.last_name(),
            "country": self._faker.country(),
            "date_of_birth": timezone.now(),
            "is_admin": True
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["success"], True)

    def test_register_with_missing_data(self):
        self.create_user_account(is_admin=True)
        self.log_user(email=self._test_email, password=self._test_password)

        response = self._client.post(self._register_url, data={
            "email": self._faker.email(),
            "password": self._faker.password()
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["success"], False)

    def test_logout_before_login(self):
        response = self._client.post(self._logout_url)

        self.assertEqual(response.status_code, 403)

    def test_logout_after_login(self):
        self.create_user_account(is_admin=True)
        self.log_user(email=self._test_email, password=self._test_password)

        response = self._client.post(self._logout_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["success"], True)

    def test_send_otp_for_invalid_user(self):
        response = self._client.post(self._send_otp, {
            "user": self._faker.email()
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["success"], False)

    def test_send_otp_for_valid_user(self):
        self.create_user_account(is_admin=True)

        response = self._client.post(self._send_otp, {
            "user": self._test_email
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["success"], True)

    def test_send_otp_one_after_another_within_two_minutes(self):
        self.create_user_account(is_admin=True)

        response = self._client.post(self._send_otp, {
            "user": self._test_email
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["success"], True)

        response = self._client.post(self._send_otp, {
            "user": self._test_email
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["success"], False)

    def test_verify_otp_with_invalid_user(self):
        response = self._client.post(self._verify_otp, {
            "email": self._test_email,
            "otp_code": 212133
        })

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["success"], False)

    def test_verify_otp_with_valid_user_and_otp(self):
        user = self.create_user_account(is_admin=True)
        self.create_otp(user)

        response = self._client.post(self._verify_otp, {
            "email": self._test_email,
            "otp_code": self._test_otp
        })

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data["data"])
        self.assertEqual(response.data["success"], True)

    def test_verify_otp_with_valid_user_and_invalid_otp(self):
        user = self.create_user_account(is_admin=True)
        self.create_otp(user)

        response = self._client.post(self._verify_otp, {
            "email": self._test_email,
            "otp_code": 291038
        })

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["success"], False)

    def test_verify_otp_with_expired_otp_code(self):
        user = self.create_user_account(is_admin=True)
        self.create_otp(user, time_delta=-2)

        response = self._client.post(self._verify_otp, {
            "email": self._test_email,
            "otp_code": self._test_otp
        })

        self.assertEqual(response.status_code, 498)
        self.assertEqual(response.data["success"], False)

    def test_forget_password_with_invalid_user(self):
        response = self._client.post(self._forget_password, {
            "email": "dewfewfew",
            "otp_id": self._test_otp,
            "password": "NewPassword"
        })

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["success"], False)

    def test_forget_password_with_invalid_otp_id(self):
        self.create_user_account(is_admin=True)

        response = self._client.post(self._forget_password, {
            "email": self._test_email,
            "otp_id": 213142,
            "password": "NewPassword"
        })

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["success"], False)

    def test_forget_password_with_valid_otp_id(self):
        user = self.create_user_account(is_admin=True)
        self.create_otp(user, time_delta=2)

        response = self._client.post(self._verify_otp, {
            "email": self._test_email,
            "otp_code": self._test_otp
        })

        response = self._client.post(self._forget_password, {
            "email": self._test_email,
            "otp_id": response.data["data"],
            "password": "NewPassword"
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["success"], True)

    def test_user_stat_with_without_login(self):
        response = self._client.get(self._user_stat)

        self.assertEqual(response.status_code, 403)

    def test_user_stat_with_with_invalid_user_type(self):
        self.create_user_account(coach=self.create_coach())
        self.log_user(email=self._test_email, password=self._test_password)

        response = self._client.get(self._user_stat)

        self.assertEqual(response.status_code, 403)

    def test_user_stat_with_with_admin(self):
        self.create_user_account(is_admin=True)
        self.log_user(email=self._test_email, password=self._test_password)

        response = self._client.get(self._user_stat)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["success"], True)
