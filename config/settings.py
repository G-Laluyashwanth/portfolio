"""
Django settings for the Portfolio project.
Environment-driven via python-decouple. Defaults to SQLite for local dev;
set DB_ENGINE=postgres or DATABASE_URL for PostgreSQL.
"""
from pathlib import Path
from urllib.parse import urlparse

from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent

# ~~~
# Core
# ~~~
DEBUG = config('DEBUG', default=True, cast=bool)
SECRET_KEY = config('SECRET_KEY', default='dev-insecure-change-me-only-for-local')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost', cast=Csv())
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default='', cast=Csv())

if not DEBUG and (
    not SECRET_KEY
    or SECRET_KEY.startswith('dev-')
    or len(SECRET_KEY) < 50
):
    raise ValueError(
        'Set a strong SECRET_KEY (50+ chars) in the environment when DEBUG=False.'
    )

# ~~~
# Applications
# ~~~
DJANGO_APPS = [
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
]

LOCAL_APPS = [
    'apps.core',
    'apps.projects',
    'apps.skills',
    'apps.experience',
    'apps.contact',
]

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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
                'apps.core.context_processors.site_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# ~~~
# Database - SQLite by default; DATABASE_URL or DB_ENGINE=postgres for Postgres
# ~~~
DATABASE_URL = config('DATABASE_URL', default='')

if DATABASE_URL:
    parsed = urlparse(DATABASE_URL)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': parsed.path.lstrip('/'),
            'USER': parsed.username or '',
            'PASSWORD': parsed.password or '',
            'HOST': parsed.hostname or '',
            'PORT': str(parsed.port or '5432'),
        }
    }
elif config('DB_ENGINE', default='').lower() == 'postgres':
    db_password = config('DB_PASSWORD', default='')
    if not db_password:
        raise ValueError('DB_PASSWORD is required when DB_ENGINE=postgres.')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME', default='portfolio'),
            'USER': config('DB_USER', default='postgres'),
            'PASSWORD': db_password,
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='5432'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ~~~
# Password validation
# ~~~
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ~~~
# i18n / tz
# ~~~
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# ~~~
# Static & Media
# ~~~
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Django 6 uses STORAGES (STATICFILES_STORAGE is ignored).
# Manifest hashing only in production - local/tests use plain storage so
# missing staticfiles.json does not break {% static %} / static().
_STATIC_BACKEND = (
    'django.contrib.staticfiles.storage.StaticFilesStorage'
    if DEBUG
    else 'whitenoise.storage.CompressedManifestStaticFilesStorage'
)
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': _STATIC_BACKEND,
    },
}

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Path under STATICFILES_DIRS for the résumé PDF (works with DEBUG=False).
RESUME_STATIC = 'resume/Lalu_Yashwanth_Resume.pdf'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ~~~
# Production security (only when DEBUG is off)
# ~~~
if not DEBUG:
    SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
    SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=31536000, cast=int)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ~~~
# Django Unfold - admin UI (structured sidebar, light/dark toggle)
# ~~~
from django.templatetags.static import static  # noqa: E402
from config.admin import UNFOLD_SIDEBAR, dashboard_callback, environment_callback  # noqa: E402

UNFOLD = {
    'SITE_TITLE': 'Portfolio Admin',
    'SITE_HEADER': 'Portfolio',
    'SITE_SUBHEADER': 'Content management',
    'SITE_URL': '/',
    'SITE_ICON': {
        'light': lambda request: static('admin-icon-light.svg'),
        'dark': lambda request: static('favicon.svg'),
    },
    'SITE_FAVICONS': [
        {
            'rel': 'icon',
            'sizes': '32x32',
            'type': 'image/svg+xml',
            'href': lambda request: static('favicon.svg'),
        },
    ],
    'BORDER_RADIUS': '8px',
    'SHOW_VIEW_ON_SITE': True,
    'ENVIRONMENT': environment_callback,
    'DASHBOARD_CALLBACK': dashboard_callback,
    'SIDEBAR': {
        'show_search': True,
        'show_all_applications': False,
        'navigation': UNFOLD_SIDEBAR,
    },
    'COLORS': {
        'base': {
            '50': '#f4f5f7',
            '100': '#e8e9eb',
            '200': '#c8cdd4',
            '300': '#9aa1aa',
            '400': '#6b7280',
            '500': '#4a4f57',
            '600': '#353940',
            '700': '#22252a',
            '800': '#16181c',
            '900': '#0e0f11',
            '950': '#080809',
        },
        'primary': {
            '50': '#eef2ff',
            '100': '#e0e7ff',
            '200': '#c7d2fe',
            '300': '#a5b4fc',
            '400': '#818cf8',
            '500': '#6366f1',
            '600': '#4f46e5',
            '700': '#4338ca',
            '800': '#3730a3',
            '900': '#312e81',
            '950': '#1e1b4b',
        },
    },
}

# ~~~
# Email (optional - kept for future use; contact form is removed)
# ~~~
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@example.com')
