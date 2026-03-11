release: python manage.py migrate --noinput
web: gunicorn portfolio_site.wsgi:application --bind 0.0.0.0:10000
