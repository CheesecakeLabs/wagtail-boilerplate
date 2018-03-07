import os
from os.path import dirname, join, exists, abspath

import environ

# Load operating system env variables and prepare to use them
env = environ.Env()

# .env file, should load only in development environment
env_file = join(dirname(__file__), 'local.env')
if exists(env_file):
    environ.Env.read_env(str(env_file))


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = dirname(dirname(abspath(__file__)))

# Quick-start development settings - unsuitable for production
SECRET_KEY = env('DJANGO_SECRET_KEY', default='8#ubdv*jh_1u(6m4)^s^*pdo!&y_#jz)vv%5cp%8^*&%ztttxq')

# SECURITY WARNING: don't run with debug turned on in production!
ENVIRONMENT = env('ENVIRONMENT')
DEBUG = env.bool('DJANGO_DEBUG', False)

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', [])

# Application definition
WAGTAIL_APPS = [
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',
    'modelcluster',
    'taggit',
]

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'storages',
    'webpack_loader',
]

PROJECT_APPS = []

INSTALLED_APPS = WAGTAIL_APPS + DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'wagtail.core.middleware.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

ROOT_URLCONF = 'app.urls'

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
            ]
        },

    },
]

WSGI_APPLICATION = 'app.wsgi.application'

# Database

DATABASES = {
    'default': env.db('DATABASE_URL', default='sqlite:///app.db'),
}

# Password validation

AUTH_PASSWORD_VALIDATORS = [{
    'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
}]

# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Email settings

if ENVIRONMENT == 'development':
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    DEFAULT_FROM_EMAIL = 'no-reply@localhost'

# Wagtail settings

WAGTAIL_SITE_NAME = "Mão na Massa"

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = 'https://example.org'

# Static and Media files

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, '.dist'),
)

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': '',
        'STATS_FILE': os.path.join(BASE_DIR, '.dist', 'webpack-stats.json'),
    }
}

if ENVIRONMENT == 'development':
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, '.public')

    MEDIA_URL = '/uploads/'
    MEDIA_ROOT = os.path.join(BASE_DIR, '.media')
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

if ENVIRONMENT in ['staging', 'production']:
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

    AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
    STATIC_URL = 'https://%s/%s' % (AWS_S3_CUSTOM_DOMAIN, 'static/')
    STATIC_ROOT = STATIC_URL

    MEDIA_URL = 'https://%s/%s' % (AWS_S3_CUSTOM_DOMAIN, 'uploads/')
    MEDIA_ROOT = MEDIA_URL
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
