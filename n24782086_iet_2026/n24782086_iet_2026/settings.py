"""
Django settings for n24782086_iet_2026 project.
Updated for Lab Session 6 - User Management & Authentication
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-g!xd@l#8egb-&1p@1r5ex9n427)d!fdf9#2dyplkhvfjg+9m)5"

DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "main_app",
    "about",
    "contacts",
    # 1. Daftarkan app usermanagement sesuai NPM kamu [cite: 17]
    "usermanagement_24782086", 
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "n24782086_iet_2026.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'], 
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "n24782086_iet_2026.wsgi.application"

# Database Configuration for PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'smartcity_db',
        'USER': 'postgres',
        'PASSWORD': 'rezaldi123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 2. Konfigurasi AUTH_USER_MODEL (Instruksi Lab 6 Poin 1) [cite: 21]
# Memberitahu Django untuk menggunakan model User dari app usermanagement kamu.
AUTH_USER_MODEL = 'usermanagement_24782086.User'

# Tambahan untuk mempermudah Step Login/Logout nantinya
LOGIN_REDIRECT_URL = 'report_list'
LOGOUT_REDIRECT_URL = 'login'