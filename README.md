## How to run
1) Create new virtual env
```sh
python3 -m venv venv
```
2) Activate virtual env
```sh
source venv/bin/activate
```
3) Install dependencies
```sh
pip install -r requirements
```
4) Populate DB
```sh
python manage.py populate
```
5) Run server
```sh
python manage.py runserver
```

## Management Commands
To populate database with game data
```sh
python manage.py populate
```

To create admin account
```sh
python manage.py create_account --type 0
```

To create player account
```sh
python manage.py create_account --type 1
```

To create coach account
```sh
python manage.py create_account --type 2
```

## API Endpoints
| Endpoint | Method | Parameters | Access Group |
| ------ | ------ | ------ | ------ | 
| http://127.0.0.1:8000/auth/login | POST | email,password | All
| http://127.0.0.1:8000/auth/register | POST | email, password, first_name, last_name, (is_admin (Bool)/coach_id/player_id) | Admin
| http://127.0.0.1:8000/auth/logout | POST | - | All
| http://127.0.0.1:8000/auth/send_otp | POST | user (Email) | All
| http://127.0.0.1:8000/auth/verify_otp | POST | email, otp_code | All
| http://127.0.0.1:8000/auth/forget_password | POST | email, otp_id, password | All
| http://127.0.0.1:8000/auth/user_stat | GET | - | Admin
|  |  | 
| http://127.0.0.1:8000/game/players | GET | - | Admin
| http://127.0.0.1:8000/game/players/by_team/<int:team_id> | GET | - | coach_and_admin
| http://127.0.0.1:8000/game/players/by_percentile/<int:team_id>/<int:percentile> | GET | - | coach_and_admin
| http://127.0.0.1:8000/game/players/by_game/<str:game_id> | GET | - | admin
| http://127.0.0.1:8000/game/players/by_id/<str:player_id> | GET | - | coach_and_admin
|  |  | 
| http://127.0.0.1:8000/game/coaches | GET | - | admin
| http://127.0.0.1:8000/game/coaches/by_player/<str:player_id> | GET | - | admin
| http://127.0.0.1:8000/game/coaches/by_team/<str:team_id> | GET | - | admin
|  |  | 
| http://127.0.0.1:8000/game/teams | GET | - | admin
| http://127.0.0.1:8000/game/teams/average/<int:team_id> | GET | - | coach_and_admin
|  |  | 
| http://127.0.0.1:8000/game/scoreboards | GET | - | All
| http://127.0.0.1:8000/scoreboards/by_tournament/<int:tournament_id> | GET | - | All
| http://127.0.0.1:8000/game/scoreboards/get_games_by_tournement/<int:tournament_id> | GET | - | All
| http://127.0.0.1:8000/game/scoreboards/get_score_by_round/<int:game_id> | GET | - | All
