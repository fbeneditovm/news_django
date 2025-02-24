#!/bin/sh

# Wait for postgres
while ! nc -z postgres 5432; do
    echo "Waiting for postgres..."
    sleep 1
done

# Apply database migrations
python manage.py makemigrations
python manage.py migrate

# Start server
exec "$@" 