#!/bin/sh

sleep 10
# Initialize the database
python manage.py makemigrations
python manage.py migrate
