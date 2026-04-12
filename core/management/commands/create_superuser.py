import sys
import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    def handle(self, *args, **options):
        sys.stderr.write('=== CREATE SUPERUSER STARTING ===\n')
        print('=== CREATE SUPERUSER STARTING ===')
        
        User = get_user_model()
        
        username = os.environ.get('DJANGO_ADMIN_USERNAME', 'Admin2')
        password = os.environ.get('DJANGO_ADMIN_PASSWORD', 'Deewan@123')
        email = os.environ.get('DJANGO_ADMIN_EMAIL', 'admin@example.com')
        
        sys.stderr.write(f'Looking for user: {username}\n')
        print(f'Looking for user: {username}')
        
        user = User.objects.filter(username=username).first()
        
        if user:
            sys.stderr.write(f'User {username} found, updating password\n')
            print(f'User {username} found, updating password')
            user.set_password(password)
            user.is_staff = True
            user.is_superuser = True
            user.save()
            sys.stderr.write(f'Password updated for {username}\n')
            print(f'Password updated for {username}')
        else:
            sys.stderr.write(f'Creating new user: {username}\n')
            print(f'Creating new user: {username}')
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            sys.stderr.write(f'Superuser {username} created\n')
            print(f'Superuser {username} created')
            
        sys.stderr.write(f'=== CREATE SUPERUSER DONE ===\n')
        print(f'=== CREATE SUPERUSER DONE ===')
