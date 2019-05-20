import os
from os.path import dirname, join, exists, abspath

import environ

# Load operating system env variables and prepare to use them
env = environ.Env()

# .env file, should load only in development environment
env_file = join(dirname(__file__), ".env")
if exists(env_file):
    environ.Env.read_env(str(env_file))


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = dirname(dirname(abspath(__file__)))

# Quick-start development settings - unsuitable for production
SECRET_KEY = env(
    "DJANGO_SECRET_KEY", default="8#ubdv*jh_1u(6m4)^s^*pdo!&y_#jz)vv%5cp%8^*&%ztttxq"
)

# SECURITY WARNING: don't run with debug turned on in production!
ENVIRONMENT = env("ENVIRONMENT")
DEBUG = env.bool("DJANGO_DEBUG", False)

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", [])

# Application definition
WAGTAIL_APPS = [
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail.core",
    "modelcluster",
    "taggit",
]

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = ["storages", "webpack_loader"]

PROJECT_APPS = []

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "wagtail.core.middleware.SiteMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

if ENVIRONMENT == "development":
    THIRD_PARTY_APPS += ["debug_toolbar"]
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
    INTERNAL_IPS = "127.0.0.1"

INSTALLED_APPS = WAGTAIL_APPS + DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "app.wsgi.application"

# Database

DATABASES = {"default": env.db("DATABASE_URL", default="sqlite:///app.db")}

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"}
]

# Internationalization

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Email settings

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "no-reply@localhost"

if ENVIRONMENT in ["staging", "production"]:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_USE_TLS = True
    EMAIL_HOST = env("MAIL_SMTP")
    EMAIL_PORT = env("MAIL_PORT")
    EMAIL_HOST_USER = env("MAIL_USER")
    EMAIL_HOST_PASSWORD = env("MAIL_PASSWORD")
    EMAIL_FROM = env("EMAIL_FROM")
    DEFAULT_FROM_EMAIL = EMAIL_FROM

# Wagtail settings

WAGTAIL_SITE_NAME = "Wagtail Boilerplate"

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = "https://example.org"

# Static files

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATICFILES_DIRS = (
    os.path.join(os.path.dirname(BASE_DIR), "bundles"),
    os.path.join(BASE_DIR, "static/assets"),
)
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

WEBPACK_LOADER = {
    "DEFAULT": {
        "BUNDLE_DIR_NAME": "",
        "STATS_FILE": os.path.join(
            os.path.dirname(BASE_DIR), "bundles", "webpack-stats.json"
        ),
    }
}

# Media files

MEDIA_URL = "/uploads/"
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "uploads")
DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

if ENVIRONMENT in ["staging", "production"]:
    AWS_REGION = env("AWS_REGION")
    AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
    DEFAULT_FILE_STORAGE = "app.s3utils.MediaRootS3Boto3Storage"

# Logs

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
        "require_debug_true": {"()": "django.utils.log.RequireDebugTrue"},
    },
    "formatters": {
        "aws": {
            "format": "%(asctime)s [%(levelname)-8s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "main_formatter": {
            "format": "%(levelname)s:%(name)s: %(message)s "
            "(%(asctime)s; %(filename)s:%(lineno)d)",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {"level": "INFO", "class": "logging.StreamHandler"},
        "null": {"class": "logging.NullHandler"},
    },
    "loggers": {
        "django.request": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
        "django": {"handlers": ["console"], "level": "WARNING", "propagate": True},
    },
}

if ENVIRONMENT in ["staging", "production"]:
    LOGGING["handlers"]["watchtower"] = {
        "level": "INFO",
        "class": "watchtower.CloudWatchLogHandler",
        "boto3_session": BOTO3_SESSION,
        "log_group": env("AWS_CLOUDWATCH_LOG_GROUP"),
        "stream_name": env("AWS_CLOUDWATCH_STREAM_NAME"),
        "formatter": "main_formatter",
        "filters": ["require_debug_false"],
    }
    LOGGING["loggers"]["django"]["handlers"].append("watchtower")
    LOGGING["loggers"]["django.request"]["handlers"].append("watchtower")
