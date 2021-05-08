from django.core.management.base import BaseCommand

from wasabi import msg
from faker import Faker

from authentication.serializers import UserCreateSerializer
from game.models import Player, Coach

import random


class Command(BaseCommand):
    def _create_user_data(self, faker: Faker, type):
        user_data = {
            "email": faker.email(),
            "password": "demo@matific",
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
        }
        if type == 0:
            user_data['is_admin'] = True
        elif type == 1:
            user_id = random.sample(list(Player.objects.all()), 1)
            user_data['player_id'] = user_id[0].id
            msg.good("Player id : {}".format(user_id[0].id))
        elif type == 2:
            user_id = random.sample(list(Coach.objects.all()), 1)
            user_data['coach_id'] = user_id[0].id
            msg.good("Coach id : {}".format(user_id[0].id))
            msg.good("Team id: {}".format(user_id[0].team.id))
        return user_data

    def create_account(self, faker: Faker, type):
        user_data = self._create_user_data(faker, type)
        user_create_serializer = UserCreateSerializer(data=user_data, context={"request": user_data})
        if user_create_serializer.is_valid():
            user = user_create_serializer.save()
            msg.good("Email: {}".format(user.email))
            msg.good("Password: demo@matific")
        else:
            msg.fail("Unable to create player account", user_create_serializer.errors)

    def handle(self, *args, **options):

        type_list = [0, 1, 2]
        type = options['type']

        if type is None or type[0] not in type_list:
            msg.fail("Invalid user account type or type missing")
            return

        fake = Faker()
        self.create_account(fake, type[0])

    def add_arguments(self, parser):
        parser.add_argument('--type', action='append', type=int)
