# FastAPI

1. Prerequisite
- Poetry
- Python >= 3.10
- Docker

2. Installation guide
- Run:
> poetry install

- Copy the content in .env.example to src/.env then fill in the value

- cd to `src` then run:
> poetry run alembic upgrade head

- Run:
> poetry run python main.py

- Navigate to your desired browser, then enter `localhost:8000`

3. Docker config guide

- Copy the content in .env.example to .env file then fill in the value 

- Copy the content in .env.db.example to .env.db.dev file

- Run:

> docker compose up

- http://localhost:8000/api/v1/docs to access the API docs
