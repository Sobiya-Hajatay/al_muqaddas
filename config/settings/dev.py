import os
from pathlib import Path
from .base import *
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# ===== Amadeus TEMP Keys =====
AMADEUS_API_KEY = "sobiya@30"
AMADEUS_API_SECRET = "sobi@30"

FLIGHT_API_KEY = "YOUR_FLIGHT_API_KEY"
FLIGHT_API_SECRET = "YOUR_FLIGHT_SECRET"

HOTEL_API_KEY = "YOUR_HOTEL_API_KEY"
HOTEL_API_SECRET = "YOUR_HOTEL_SECRET"

# ================= CACHE (ENTERPRISE) =================
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "almuqaddas-cache",
        "TIMEOUT": 60 * 10,  # 10 minutes
    }
}
DEBUG = True

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    ".onrender.com",
    ".railway.app",
    ".vercel.app",
]
RAZORPAY_KEY_ID = "rzp_test_SM5TczGBVJD9FC"
RAZORPAY_KEY_SECRET = "L5Yg1ZbElZW4SKO2NshpxsUC"