#!/usr/bin/env bash
# Script to create Django superuser
# Usage: Set environment variables and run this script

# Check if password is set
if [ -z "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "Error: DJANGO_SUPERUSER_PASSWORD environment variable is required"
    echo "Set these environment variables:"
    echo "  DJANGO_SUPERUSER_USERNAME (default: admin)"
    echo "  DJANGO_SUPERUSER_EMAIL (default: admin@example.com)"
    echo "  DJANGO_SUPERUSER_PASSWORD (required)"
    exit 1
fi

# Run the Python script
python create_superuser.py

