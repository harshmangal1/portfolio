import sys
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        
        if User.objects.filter(username='Admin2').exists():
            print('Superuser Admin2 already exists')
            sys.stderr.write('Superuser Admin2 already exists\n')
            return
            
        user = User.objects.create_superuser(
            username='Admin2',
            email='admin@example.com',
            password='Deewan@123'
        )
        print(f'Superuser Admin2 created successfully with password Deewan@123')
        sys.stderr.write(f'Superuser created: {user.username}\n')
