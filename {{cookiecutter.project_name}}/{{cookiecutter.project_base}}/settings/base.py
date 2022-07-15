"""
Base settings for {{ cookiecutter.project_title }}
"""
from typing import Tuple
from pathlib import Path

from django.utils.translation import gettext_lazy as _
import structlog
import environ


# =================================
# CONFIG SETUP
# =================================
# Build paths : BASE_DIR / 'subdir'.
BASE_DIR: str = Path(__file__).resolve(strict=True).parent.parent.parent
APPS_DIR: str = BASE_DIR / "{{ cookiecutter.project_base }}"

env = environ.Env()

READ_DOT_ENV_FILE: bool = env.bool("READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    # Read environment variables from .env
    env.read_env(str(BASE_DIR / ".env"))

# =================================
# GENERAL CONFIG
# =================================
SECRET_KEY: str = env('DJANGO_SECRET_KEY')
DEBUG: bool = env.bool("DEBUG", False)

# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID: int = 1

# =================================
# INTERNATIONALIZATION
# =================================
LANGUAGE_CODE: str = 'en-us'
LANGUAGES: Tuple[Tuple[str, ...]] = (
    ('en', _('English')),
)
# https://docs.djangoproject.com/en/3.2/topics/i18n/
USE_I18N: bool = True
USE_L10N: bool = True

USE_TZ: bool = True
TIME_ZONE: str = 'UTC'


# =================================
# URLS CONFIG
# =================================
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF: str = "{{ cookiecutter.project_base }}.urls"
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION: str = "{{ cookiecutter.project_base }}.wsgi.application"


# ================================
# DJANGO APPS
# ================================
DJANGO_APPS: list[str] = [
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
THIRD_PARTY_APPS: list[str] = [
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "crispy_forms",
    "crispy_bootstrap5",
    "sorl.thumbnail",
    {%- if cookiecutter.use_htmx == 'y' or cookiecutter.use_htmx == 'yes' %}
    "django_htmx",
    {%- endif %}
]
LOCAL_APPS: list[str] = [
    "apps.users.apps.UsersConfig",
]

# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS: list[str] = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


# ================================
# AUTHENTICATION
# ================================
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods
    "allauth.account.auth_backends.AuthenticationBackend",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = "apps.users.User"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = "users:redirect"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = "account_login"

# ================================
# DJANGO MIDDLEWARES
# ================================
MIDDLEWARE: Tuple[str, ...] = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    {%- if cookiecutter.use_htmx == 'y' or cookiecutter.use_htmx == 'yes' %}
    'django_htmx.middleware.HtmxMiddleware',
    {%- endif %}
    'django_structlog.middlewares.RequestMiddleware',
)

# ================================
# STATIC CONFIG
# ================================
STATIC_URL: str = "/static/"
STATICFILES_DIRS: list[str] = [BASE_DIR / "static"]
STATIC_ROOT: str = BASE_DIR / "staticfiles"
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS: list[str] = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# ================================
# MEDIA CONFIG
# ================================
MEDIA_URL: str = "/media/"
MEDIA_ROOT: str = BASE_DIR / "media"

# ================================
# TEMPLATES CONFIG
# ================================
TEMPLATES: list[dict] = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # `allauth` needs this from django
                "django.template.context_processors.request",
                "apps.users.context_processors.allauth_settings",
            ],
        },
    },
]

# https://docs.djangoproject.com/en/dev/ref/settings/#form-renderer
FORM_RENDERER: str = "django.forms.renderers.TemplatesSetting"

# ================================
# SECURITY
# ================================
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]

# https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-DEFAULT_AUTO_FIELD
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ================================
# ADMIN CONFIG
# ================================
ADMIN_URL: str = "admin/"

# ================================
# Django Crispy Form
# ================================
# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK: str = "bootstrap5"
CRISPY_ALLOWED_TEMPLATE_PACKS: str = "bootstrap5"

# ================================
# Django-allauth CONFIG
# ================================
# https://django-allauth.readthedocs.io/en/latest/configuration.html
# LOGIN_REDIRECT_URL = "/"
ACCOUNT_EMAIL_REQUIRED: bool = True
ACCOUNT_ADAPTER: str = "apps.users.adapters.AccountAdapter"
ACCOUNT_FORMS: dict = {"signup": "apps.users.forms.UserSignupForm"}
SOCIALACCOUNT_ADAPTER = "apps.users.adapters.SocialAccountAdapter"
# SOCIALACCOUNT_FORMS = {"signup": "apps.users.forms.UserSocialSignupForm"}
# ACCOUNT_ALLOW_REGISTRATION = env.bool("ALLOW_REGISTRATION", True)
# ACCOUNT_AUTHENTICATION_METHOD = "username"
# ACCOUNT_EMAIL_VERIFICATION = "mandatory"
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
{% if cookiecutter.frontend_compressor == 'Django Compressor' -%}
# https://django-compressor.readthedocs.io/en/latest/quickstart/#installation
INSTALLED_APPS += ["compressor"]
STATICFILES_FINDERS += ["compressor.finders.CompressorFinder"]
{%- endif %}

# ================================
# LOGGING CONFIG
# ================================
# https://docs.djangoproject.com/en/dev/ref/settings/#logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'json_formatter': {
            '()': structlog.stdlib.ProcessorFormatter,
            'processor': structlog.processors.JSONRenderer(),
        },
        'console': {
            '()': structlog.stdlib.ProcessorFormatter,
            'processor': structlog.processors.KeyValueRenderer(
                key_order=['timestamp', 'level', 'event', 'logger'],
            ),
        },
    },

    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
        'json_console': {
            'class': 'logging.StreamHandler',
            'formatter': 'json_formatter',
        },
    },

    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
    },
}

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.processors.TimeStamper(fmt='iso'),
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.ExceptionPrettyPrinter(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    context_class=structlog.threadlocal.wrap_dict(dict),
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)
