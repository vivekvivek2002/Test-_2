#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status
set -o errexit

echo "--- Installing dependencies ---"
pip install -r requirements.txt

echo "--- Collecting static assets ---"
python manage.py collectstatic --no-input

echo "--- Running database migrations ---"
python manage.py migrate

echo "--- Build completed successfully ---"
