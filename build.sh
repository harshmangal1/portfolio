#!/usr/bin/env bash
# Run migrations and collectstatic before starting gunicorn
set -e

pip install -r requirements.txt

python manage.py migrate --noinput
python manage.py collectstatic --noinput --ignore='*.txt'
python manage.py create_superuser

exec gunicorn portfolio_site.wsgi:application
