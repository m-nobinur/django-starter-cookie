import os
from typing import Optional
{% if cookiecutter.use_heroku == 'y' %}
import dj_database_url
{% endif %}

from .base import *  # noqa F405

# ==============================
# GENERAL PRODUCTION CONFIG
# ==============================
DEBUG = False
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list(  # noqa F405
    "DJANGO_ALLOWED_HOSTS", default=["example-domain.com"]
)

# ==============================
# DATABASES
# ==============================
{% if cookiecutter.use_heroku == 'y' %}
DATABASES = {"default": dj_database_url.config(conn_max_age=600)}
# DATABASES = {"default": dj_database_url.parse(os.environ.get("DATABASE_URL"))}
{% else %}
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": os.environ.get("DJANGO_DATABASE_HOST"),
        "PORT": os.environ.get("DJANGO_DATABASE_PORT"),
        "CONN_MAX_AGE": os.environ.get("CONN_MAX_AGE", default=60),
        "OPTIONS": {
            "connect_timeout": 10,
            "options": "-c statement_timeout=15000ms",
        },
    },
}
{% endif %}

# ==============================
# CACHES
# ==============================
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# ==============================
# SECURITY
# ==============================
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = os.environ.get("DJANGO_SECURE_SSL_REDIRECT", default=True)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# ==============================
# Password validation
# ==============================
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ==============================
# STORAGES
# ==============================
{% if cookiecutter.cloud_provider != 'None' -%}
INSTALLED_APPS += ["storages"]  # noqa F405
{%- endif -%}
{% if cookiecutter.cloud_provider == 'AWS' %}
# =============================
# AWS S3 configuration
# =============================
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME")

_AWS_EXPIRY = 60 * 60 * 24 * 7
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": f"max-age={_AWS_EXPIRY}, s-maxage={_AWS_EXPIRY}, must-revalidate"
}
AWS_QUERYSTRING_AUTH = False

AWS_S3_CUSTOM_DOMAIN = os.environ.get("DJANGO_AWS_S3_CUSTOM_DOMAIN", default=None)
S3_DOMAIN = AWS_S3_CUSTOM_DOMAIN or f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"

STATICFILES_STORAGE = "{{ cookiecutter.project_base }}.utils.storages.StaticRootS3Boto3Storage"
COLLECTFAST_STRATEGY = "collectfast.strategies.boto3.Boto3Strategy"
STATICFILES_LOCATION = "static"
DEFAULT_FILE_STORAGE = "{{ cookiecutter.project_base }}.utils.storages.MediaRootS3Boto3Storage"
MEDIAFILES_LOCATION = "media"

STATIC_URL = f"https://{S3_DOMAIN}/{STATICFILES_LOCATION}/"
MEDIA_URL = f"https://{S3_DOMAIN}/{MEDIAFILES_LOCATION}/"

AWS_S3_FILE_OVERWRITE = False

{% elif cookiecutter.cloud_provider == 'GCP' %}
GS_BUCKET_NAME = env("DJANGO_GCP_STORAGE_BUCKET_NAME")  # noqa: F405
GS_DEFAULT_ACL = "publicRead"
STATICFILES_STORAGE = "{{cookiecutter.project_slug}}.utils.storages.StaticRootGoogleCloudStorage"
COLLECTFAST_STRATEGY = "collectfast.strategies.gcloud.GoogleCloudStrategy"
STATIC_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/static/"
DEFAULT_FILE_STORAGE = "{{cookiecutter.project_slug}}.utils.storages.MediaRootGoogleCloudStorage"
MEDIA_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/media/"
{% endif -%}

{% if cookiecutter.use_whitenoise == 'y' -%}
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
{% endif -%}

{% if cookiecutter.mail_service == 'Gmail' -%}
# ===================================
# EMAIL SMTP SERVER CONFIGURATION
# ===================================
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_PORT = os.environ.get("EMAIL_PORT", 587)
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", True)
{% endif %}

{% if cookiecutter.use_mailchimp == 'y' -%}
# ========================
# Mailchimp Configuration
# ========================
MAILCHIMP_API_KEY = os.environ.get("MAILCHIMP_API_KEY")
MAILCHIMP_DATA_CENTER = os.environ.get("MAILCHIMP_DATA_CENTER")
MAILCHIMP_EMAIL_LIST_ID = os.environ.get("MAILCHIMP_EMAIL_LIST_ID")
{% endif %}

# ==============================
# ADMIN URL CONFIG
# ==============================
ADMIN_URL: Optional[str] = os.environ.get("DJANGO_ADMIN_URL") # type: ignore

# ==============================
# django-compressor
# ==============================
{%- if cookiecutter.cloud_provider == 'None' %}
# https://django-compressor.readthedocs.io/en/latest/settings/#django.conf.settings.COMPRESS_STORAGE
COMPRESS_STORAGE = "compressor.storage.GzipCompressorFileStorage"
{%- elif cookiecutter.cloud_provider in ('AWS', 'GCP') and cookiecutter.use_whitenoise == 'n' %}
COMPRESS_STORAGE = STATICFILES_STORAGE
{%- endif %}
COMPRESS_URL = STATIC_URL # noqa: F405
{% if cookiecutter.use_whitenoise == 'y' %}
COMPRESS_OFFLINE = True
COMPRESS_FILTERS = {
    "css": [
        "compressor.filters.css_default.CssAbsoluteFilter",
        "compressor.filters.cssmin.rCSSMinFilter",
    ],
    "js": ["compressor.filters.jsmin.JSMinFilter"],
}
{% endif %}

{% if cookiecutter.use_whitenoise == 'n' %}
# https://github.com/antonagestam/collectfast#installation
INSTALLED_APPS = ["collectfast"] + INSTALLED_APPS  # noqa: F405
{% endif %}
