release: python manage.py migrate --noinput && python manage.py create_superuser
web: gunicorn portfolio_site.wsgi:application
