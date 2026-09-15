import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "serveease.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = os.environ.get("ADMIN_USERNAME", "admin")
email = os.environ.get("ADMIN_EMAIL", "admin@serveease.com")
password = os.environ.get("ADMIN_PASSWORD")

if not password:
    print("ADMIN_PASSWORD is not set.")
else:
    if User.objects.filter(username=username).exists():
        print("Admin already exists.")
    else:
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print("Admin created successfully.")