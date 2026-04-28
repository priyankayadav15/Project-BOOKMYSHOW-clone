"""
Django settings for bookmyseat project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent
env_path = os.path.join(BASE_DIR, ".env")

# Load env
load_dotenv(dotenv_path=env_path, override=True)

# SECURITY
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "True") == "True"

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "bookmyseat-3wse.onrender.com",
    ".vercel.app"
]

# =====================
# APPLICATIONS
# =====================
INSTALLED_APPS = [
    'jazzmin',   # ✅ MUST be first
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'users',
    'movies',
]

# =====================
# MIDDLEWARE
# =====================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTH_USER_MODEL = 'auth.User'

# =====================
# EMAIL (SENDGRID)
# =====================
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "apikey"
EMAIL_HOST_PASSWORD = os.getenv("SENDGRID_API_KEY")

DEFAULT_FROM_EMAIL = "BookMySeat <priyanka111010@gmail.com>"

# =====================
# MEDIA
# =====================
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# =====================
# URLS
# =====================
ROOT_URLCONF = 'bookmyseat.urls'
LOGIN_URL = '/login/'

# =====================
# TEMPLATES
# =====================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'bookmyseat.wsgi.application'

# =====================
# DATABASE
# =====================
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR}/db.sqlite3",
        conn_max_age=600,
        ssl_require=False
    )
}

# =====================
# PASSWORD VALIDATION
# =====================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# =====================
# INTERNATIONAL
# =====================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# =====================
# STATIC FILES
# =====================
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =====================
# STRIPE
# =====================
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")

# =====================
# CSRF
# =====================
CSRF_TRUSTED_ORIGINS = [
    "https://*.onrender.com",
    "https://*.vercel.app"
]

# =====================
# JAZZMIN (🔥 ALWAYS ACTIVE)
# =====================
JAZZMIN_SETTINGS = {
    "site_title": "BookMySeat Admin",
    "site_header": "BookMySeat Dashboard",
    "site_brand": "BookMySeat",
    "welcome_sign": "Welcome to BookMySeat Admin",

    # ✅ LOGO (put inside static/images/logo.png)
    "site_logo": "images/logo.png",

    # ✅ TOP MENU (THIS FIXES YOUR PROBLEM)
    "topmenu_links": [
        {"name": "Dashboard", "url": "/admin-dashboard/"},
        {"name": "Home", "url": "/"},
    ],

    # ✅ ICONS
    "icons": {
        "movies.movie": "fas fa-film",
        "movies.theater": "fas fa-building",
        "movies.seat": "fas fa-chair",
        "movies.booking": "fas fa-ticket-alt",
        "auth.user": "fas fa-user",
    },

    "show_sidebar": True,
    "navigation_expanded": True,
}

# =====================
# PRODUCTION SECURITY
# =====================
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True