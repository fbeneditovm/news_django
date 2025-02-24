#!/bin/sh

# Wait for postgres to be ready
while ! nc -z postgres 5432; do
    echo "Waiting for postgres..."
    sleep 1
done

# Wait a bit more to ensure postgres is fully ready
sleep 5

# Apply database migrations
python manage.py makemigrations
python manage.py migrate

# Execute the command passed to docker run
exec "$@" 