import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')

application = get_wsgi_application()

from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin2').exists():
    User.objects.create_superuser('admin2', 'admin2@example.com', 'admin123456')
