"""
Django settings for n24782086_iet_2026 project.
Updated for Lab Session 6 - User Management & Authentication
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-g!xd@l#8egb-&1p@1r5ex9n427)d!fdf9#2dyplkhvfjg+9m)5"

DEBUG = True

ALLOWED_HOSTS = ['*']

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
    "usermanagement_24782086",
    'rest_framework_simplejwt',
    'corsheaders',
    'rest_framework',
    'dashboard_24782086',
    'drf_spectacular',
    'django_scalar',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = 'smartcity_app.urls'

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

WSGI_APPLICATION = 'smartcity_app.wsgi.application'

import sys

# Database Configuration for PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'db_mhs04',
        'USER': 'user_mhs04',
        'PASSWORD': 'mhs04',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Gunakan SQLite secara otomatis jika sedang menjalankan pengujian
if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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

# --- KONFIGURASI STATIC FILES ---
STATIC_URL = "static/"
# Jalur folder untuk menampung seluruh static files saat Production di Server
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 2. Konfigurasi AUTH_USER_MODEL (Instruksi Lab 6 Poin 1)
# Memberitahu Django untuk menggunakan model User dari app usermanagement kamu.
AUTH_USER_MODEL = 'usermanagement_24782086.User'

# Tambahan untuk mempermudah Step Login/Logout nantinya
LOGIN_REDIRECT_URL = 'report_list'
LOGOUT_REDIRECT_URL = 'login'

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

CORS_ALLOW_ALL_ORIGINS = True

# Konfigurasi CSRF Trusted Origins agar Form Login/Register tidak diblokir Django 4.x
CSRF_TRUSTED_ORIGINS = [
    'http://103.151.63.88:8004',
    'https://iet-polinela.github.io',
]

# Taruh ini di baris paling akhir file settings.py kamu
SPECTACULAR_SETTINGS = {
    'TITLE': 'Smart City Portal API',
    'DESCRIPTION': 'Dokumentasi REST API resmi untuk Portal Pelaporan Laporan Warga',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SECURITY': [
        {
            'Bearer': [],
        }
    ],
    'COMPONENT_SPLIT_REQUEST': True,
}