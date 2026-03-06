from .base import *
import os
import dj_database_url

DEBUG = False

ALLOWED_HOSTS = [
    "almuqaddas.in",
    "www.almuqaddas.in",
    "127.0.0.1",
    ".railway.app"
]

# Security
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# Static
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Media
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# PostgreSQL (Railway database)
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL")
    )
}