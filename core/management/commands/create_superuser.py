import sys
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    def handle(self, *args, **options):
        print('Running create_superuser command...', file=sys.stderr)
        User = get_user_model()
        if not User.objects.filter(username='Admin2').exists():
            User.objects.create_superuser('Admin2', 'admin@example.com', 'Deewan@123')
            self.stdout.write(self.style.SUCCESS('Superuser Admin2 created'))
        else:
            print('Superuser Admin2 already exists', file=sys.stderr)
