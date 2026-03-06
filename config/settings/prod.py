from .base import *
import os

DEBUG = False

ALLOWED_HOSTS = [
    "almuqaddas.in",
    "www.almuqaddas.in",
    "127.0.0.1"
]

# ✅ Security
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# ✅ Static
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# ✅ Media
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# ✅ PostgreSQL (production DB)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "almuqaddas_db",
        "USER": "postgres",
        "PASSWORD": "sobi123",
        "HOST": "localhost",
        "PORT": "5432",
    }
}