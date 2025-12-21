#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Verify gunicorn is installed (reinstall if needed)
python -c "import gunicorn" 2>/dev/null || pip install gunicorn==21.2.0

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate --noinput

# Create superuser automatically with hardcoded credentials
echo "Creating superuser..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
username = 'kljeweller@gmail.com'
email = 'kljeweller@gmail.com'
password = 'kl@9090'
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Successfully created superuser: {username}')
else:
    print(f'Superuser {username} already exists. Skipping creation.')
EOF
