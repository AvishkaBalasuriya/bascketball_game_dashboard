from django.urls import path

from .views import player, scoreboard, coach, team

urlpatterns = [
    # Players
    path('players', player.get_all, name="get_all_players"),
    path('players/by_team/<int:team_id>', player.get_by_team, name="get_players_by_team"),
    path('players/by_percentile/<int:team_id>/<int:percentile>', player.get_by_percentile,
         name="get_players_by_percentile"),
    path('players/by_game/<str:game_id>', player.get_by_game,
         name="get_players_by_game"),
    path('players/by_id/<str:player_id>', player.get_by_player_id, name="get_player_by_player_id"),

    # Coaches
    path('coaches', coach.get_all, name="get_all_coaches"),
    path('coaches/by_player/<str:player_id>', coach.get_by_player, name="get_coaches_by_player"),
    path('coaches/by_team/<str:team_id>', coach.get_by_team, name="get_coaches_by_team"),

    # Teams
    path('teams', team.get_all, name="get_all_teams"),
    path('teams/average', team.get_teams_average, name="get_teams_average"),
    path('teams/average/<int:team_id>', team.get_team_average, name="get_team_average"),

    # Scoreboard
    path('scoreboards', scoreboard.get_all, name="get_all_scoreboard"),
    path('scoreboards/by_tournament/<int:tournement_id>', scoreboard.get_by_tournament_id,
         name="get_scoreboard_by_tournament_id"),
    path('scoreboards/get_games_by_tournement/<int:tournement_id>', scoreboard.get_all_games_by_tournament,
         name="get_all_games_by_tournament"),
    path('scoreboards/get_score_by_round/<int:game_id>', scoreboard.get_score_by_round,
         name="get_game_score_by_round"),
]
