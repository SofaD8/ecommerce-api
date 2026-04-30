#!/bin/bash

echo "Waiting for postgres..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

alembic revision --autogenerate -m "auto_migration" || echo "No changes detected in models"

echo "Applying migrations..."
alembic upgrade head

exec "$@"
