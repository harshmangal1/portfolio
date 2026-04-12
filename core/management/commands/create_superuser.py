import sys
import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        
        username = os.environ.get('DJANGO_ADMIN_USERNAME', 'Admin2')
        password = os.environ.get('DJANGO_ADMIN_PASSWORD', 'Deewan@123')
        email = os.environ.get('DJANGO_ADMIN_EMAIL', 'admin@example.com')
        
        if User.objects.filter(username=username).exists():
            print(f'Superuser {username} already exists')
            sys.stderr.write(f'Superuser {username} already exists\n')
            return
            
        try:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            print(f'Superuser {username} created successfully')
            print(f'Password: {password}')
            sys.stderr.write(f'Superuser created: {user.username}\n')
        except Exception as e:
            print(f'Error creating superuser: {e}')
            sys.stderr.write(f'Error: {e}\n')
            raise
