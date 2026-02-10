#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Create superuser if none exists
python manage.py create_superuser_if_none

# Import packages if needed
python manage.py import_packages

# Fetch images for packages (force re-download to ensure files exist)
python manage.py fetch_package_images --images-per-package=5 --force
