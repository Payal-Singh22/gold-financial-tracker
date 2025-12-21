#!/usr/bin/env bash
# Exit on error
set -o errexit

# Run migrations (in case of any pending migrations)
python manage.py migrate --noinput

# Start Gunicorn using Python module syntax (more reliable)
python -m gunicorn jewellery_billing.wsgi:application --bind 0.0.0.0:$PORT
