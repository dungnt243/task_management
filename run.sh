#! /bin/bash

# Run migration
poetry run alembic upgrade head

# Start server
poetry run python main.py
