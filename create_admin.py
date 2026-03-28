import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.accounts.models import User

if not User.objects.filter(username="admin").exists():
    user = User.objects.create(username="admin", email="admin@gmail.com")
    user.set_password("admin123")
    user.is_superuser = True
    user.is_staff = True
    user.save()
    print("Superuser created successfully")
else:
    print("Superuser already exists")