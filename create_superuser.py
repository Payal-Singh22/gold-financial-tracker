#!/usr/bin/env python
"""
Script to create Django superuser using environment variables.
Run this as a one-time command on Render or locally.
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jewellery_billing.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Get credentials from environment variables
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

if not password:
    print("Error: DJANGO_SUPERUSER_PASSWORD environment variable is required")
    print("Usage: Set DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, and DJANGO_SUPERUSER_PASSWORD")
    sys.exit(1)

# Check if user already exists
if User.objects.filter(username=username).exists():
    print(f"Superuser '{username}' already exists. Skipping creation.")
    sys.exit(0)

# Create superuser
try:
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Successfully created superuser: {username}")
    print(f"Email: {email}")
except Exception as e:
    print(f"Error creating superuser: {e}")
    sys.exit(1)

