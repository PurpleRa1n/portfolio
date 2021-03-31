# Required:
 - docker
 - python 3.8

# Local setup  
`$ virtualenv .venv`  
`$ source .venv/bin/activate` 
`$ pip install -r requirements/dev.txt`  
`$ docker-compose -f docker-compose.local.yaml up -d` 
`$ python main.py runserver`  

# Local setup in docker
Just run command bellow to spin up a whole environment.
`$ docker-compose -f docker-compose.local.yaml up -d` 
Health check available under: http://localhost:8000/health-check/

# Auto create new migrations
1. Import your declared model into `alembic/env.py` file  
2. Run `$ alembic revision -m "{PUT MIGRATION FILE NAME HERE}" --autogenerate --head head`  
The command above will create a brand new migrations file in `alembic/versions` folder.
3. Run `$ alembic upgrade head`
This will apply migrations to database.

# Test
To run tests with coverage use:
`$ pytest -vv`
Also available a code analyzer tools:
`$ prospector`

# How to?
- To create a new user:  
{"username": "hello" "password": "world"} POST localhost:8000/api/v1/auth/registration/

- To obtain a user token, this token should be attached to any game request in `Authorization` header:  
"username": "hello" "password": "world"} POST localhost:8000/api/v1/auth/login/

- To start a new game, you need to send a request to:   
{} POST localhost:8000/api/v1/tic-tac-toe/  

- To make a move:  
{'row': 1 'col': 1} PATCH localhost:8000/api/v1/tic-tac-toe/{:game_id}/

- Retrieve the game stat:  
GET localhost:8000/api/v1/tic-tac-toe/{:game_id}/stats/  

- Retrieve user game stats:  
GET localhost:8000/api/v1/tic-tac-toe/user-stats/  
