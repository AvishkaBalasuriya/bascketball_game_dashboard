from django.contrib import admin

from .models import Game, Stage, Player, PlayerRoundScore, TeamRoundScore, Team, Tournament, Coach, Round

admin.site.register(Game)
admin.site.register(Stage)
admin.site.register(Player)
admin.site.register(PlayerRoundScore)
admin.site.register(TeamRoundScore)
admin.site.register(Tournament)
admin.site.register(Coach)
admin.site.register(Round)
admin.site.register(Team)
