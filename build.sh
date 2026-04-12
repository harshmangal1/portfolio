#!/usr/bin/env bash
# Run migrations and collectstatic before starting gunicorn
set -e

pip install -r requirements.txt

python manage.py migrate --noinput
python manage.py collectstatic --noinput --ignore='*.txt'

exec gunicorn portfolio_site.wsgi:application
