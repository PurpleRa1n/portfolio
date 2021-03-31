# Required:
 - docker
 - python 3.8

# Local setup  
`$ virtualenv .venv`  
`$ source .venv/bin/activate` 
`$ pip install -r requirements/dev.txt`  
`$ docker-compose -f docker-compose.local.yaml up -d` 
`$ python main.py runserver`  

# Auto create new migrations
1. Import your declared model into `alembic/env.py` file  
2. Run `$ alembic revision -m "{PUT MIGRATION FILE NAME HERE}" --autogenerate --head head`  
The command above will create a brand new migrations file in `alembic/versions` folder.
3. Run `$ alembic upgrade head`
This will apply migrations to database.
