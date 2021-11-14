#!/bin/bash
# This file is used to start up the Django server.

# Collect static files.
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Apply database migrations.
echo "Applying database migrations..."
python manage.py migrate

# Start the server.
echo "Starting Django server..."
python manage.py runserver 0.0.0.0:3000
