from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username='admin2').exists():
            User.objects.create_superuser('admin2', 'admin2@example.com', 'admin123456')
            self.stdout.write(self.style.SUCCESS('Superuser admin2 created'))
        else:
            self.stdout.write('Superuser admin2 already exists')
