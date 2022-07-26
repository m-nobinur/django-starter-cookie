"""Base settings for Awesome Django Project."""
import os
from pathlib import Path
from typing import Union

import environ
import structlog
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

# =================================
# CONFIG SETUP
# =================================
# Build paths : BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
APPS_DIR = BASE_DIR / "{{ cookiecutter.project_base }}"

env = environ.Env()

READ_DOT_ENV_FILE: bool = env.bool("READ_DOT_ENV_FILE", default=True)
if READ_DOT_ENV_FILE:  # pragma: no cover
    # Read environment variables from .env
    env.read_env(str(BASE_DIR / ".env"))

# =================================
# GENERAL CONFIG
# =================================
SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG: bool = env.bool("DEBUG", True)

# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID: int = 1

# =================================
# INTERNATIONALIZATION
# =================================
LANGUAGE_CODE = "en-us"
LANGUAGES: tuple[tuple[str, ...]] = (("en", _("English")),)
# https://docs.djangoproject.com/en/3.2/topics/i18n/
USE_I18N: bool = True
USE_L10N: bool = True

USE_TZ: bool = True
TIME_ZONE = "UTC"

# =================================
# URLS CONFIG
# =================================
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "{{ cookiecutter.project_base }}.urls"
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "{{ cookiecutter.project_base }}.wsgi.application"

# ================================
# DJANGO APPS
# ================================
DJANGO_APPS = [
    # Admin Interface
    "admin_interface",
    "colorfield",
    # Core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.sitemaps",
]
THIRD_PARTY_APPS = [
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "crispy_forms",
    "crispy_tailwind",
    "sorl.thumbnail",
    {%- if cookiecutter.use_htmx == 'y' or cookiecutter.use_htmx == 'yes' %}
    "django_htmx",
    {%- endif %}
]
LOCAL_APPS = [
    "users.apps.UsersConfig",
]

# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# ================================
# AUTHENTICATION
# ================================
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods
    "allauth.account.auth_backends.AuthenticationBackend",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = "users.User"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
# LOGIN_URL = "account_login"

# ================================
# DJANGO MIDDLEWARES
# ================================
MIDDLEWARE: list[str] = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_structlog.middlewares.RequestMiddleware",
    {% if cookiecutter.use_htmx == 'y' or cookiecutter.use_htmx == 'yes' %}
    "django_htmx.middleware.HtmxMiddleware",
    {% endif %}
]

# ================================
# STATIC CONFIG
# ================================
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# ================================
# MEDIA CONFIG
# ================================
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media/"

# ================================
# TEMPLATES CONFIG
# ================================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # `allauth` needs this from django
                "django.template.context_processors.request",
            ],
        },
    },
]

# ================================
# SECURITY
# ================================
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# X_FRAME_OPTIONS = "SAMEORIGIN"
# SILENCED_SYSTEM_CHECKS = ["security.W019"]

# https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-DEFAULT_AUTO_FIELD
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ================================
# ADMIN CONFIG
# ================================
ADMIN_URL = "admin/"

# ================================
# Django Crispy Form
# ================================
# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = "tailwind"
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"

# ================================
# Django-allauth CONFIG
# ================================
# https://django-allauth.readthedocs.io/en/latest/configuration.html
# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = "/"
ACCOUNT_EMAIL_REQUIRED: bool = True
# ACCOUNT_ADAPTER = "apps.users.adapters.AccountAdapter"
ACCOUNT_FORMS = {
    "login": "users.forms.UserLoginForm",
    "signup": "users.forms.UserSignupForm",
}

# SOCIALACCOUNT_ADAPTER = "apps.users.adapters.SocialAccountAdapter"
# SOCIALACCOUNT_FORMS = {"signup": "apps.users.forms.UserSocialSignupForm"}
# ACCOUNT_ALLOW_REGISTRATION = env.bool("ALLOW_REGISTRATION", True)

ACCOUNT_USER_MODEL_USERNAME_FIELD: Union[str, None] = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"  # (”username” | “email” | “username_email”)
# ACCOUNT_EMAIL_VERIFICATION = "mandatory" # ('optional' | 'mandatory' | none)
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True
ACCOUNT_LOGOUT_REDIRECT_URL = "/"
# ACCOUNT_SESSION_REMEMBER = None
ACCOUNT_SIGNUP_REDIRECT_URL = reverse_lazy("account_email_verification_sent")
# ACCOUNT_USERNAME_MIN_LENGTH = 3
# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#         # For each OAuth based provider, either add a ``SocialApp``
#         # credentials, or list them here:
#         'APP': {
#             'client_id': '123',
#             'secret': '456',
#             'key': ''
#         }
#     }
# }

# ================================
# Django-compressor CONFIG
# ================================
# https://django-compressor.readthedocs.io/en/latest/quickstart/#installation
INSTALLED_APPS += ["compressor"]

COMPRESS_ENABLED: Union[str, bool] = os.environ.get("COMPRESS_ENABLED", default=True)
COMPRESS_ROOT = BASE_DIR / "static"
STATICFILES_FINDERS += ["compressor.finders.CompressorFinder"]

# ================================
# LOGGING CONFIG
# ================================
# https://docs.djangoproject.com/en/dev/ref/settings/#logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json_formatter": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(),
        },
        "plain_console": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.dev.ConsoleRenderer(),
        },
        "key_value": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.KeyValueRenderer(key_order=['timestamp', 'level', 'event', 'logger']),
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "plain_console",
        },
    },
    "loggers": {
        "django_structlog": {
            "handlers": ["console"],
            "level": "INFO",
        },
    }
}

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    context_class=structlog.threadlocal.wrap_dict(dict),
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)
