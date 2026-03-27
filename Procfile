release: python manage.py makemigrations portfolio --noinput && python manage.py migrate --noinput && python manage.py collectstatic --noinput
web: gunicorn portfolio_site.wsgi:application --bind 0.0.0.0:10000
