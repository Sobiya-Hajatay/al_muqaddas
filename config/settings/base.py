from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = 'change-this-secret'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'jazzmin',
    
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'apps.accounts',
    'apps.core',
   

     'apps.bookings',
     'apps.invoices',
     'apps.packages',
     'apps.flights',
     "apps.hotels",
  
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',  # 👈 yaha hona chahiye

    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]


ROOT_URLCONF = 'config.urls'

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

AUTH_USER_MODEL = 'accounts.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
JAZZMIN_SETTINGS = {
    "site_title": "Al Muqaddas Admin",
    "site_header": "Al Muqaddas Tours & Travels",
    "site_brand": "Al Muqaddas",

    "welcome_sign": "Welcome to Al Muqaddas Control Room",

    "topmenu_links": [
        {"name": "Website", "url": "https://www.almuqaddas.in", "new_window": True},
    ],

    "show_sidebar": True,
    "navigation_expanded": True,

    "icons": {
        "accounts.User": "fas fa-users",
        "packages.Package": "fas fa-kaaba",
        "bookings.Booking": "fas fa-ticket-alt",
        "payments.Payment": "fas fa-money-bill",
        "invoices.Invoice": "fas fa-file-invoice",
    },
}
