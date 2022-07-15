from .base import *  # noqa
from .base import env

# ==============================
# GENERAL CONFIG
# ==============================
DEBUG = True
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS: list[str] = ["localhost", "0.0.0.0", "127.0.0.1"]

# ==============================
# Database
# ==============================
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DATABASES: dict = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

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
# django-debug-toolbar
# ==============================
INSTALLED_APPS += [
    "django_extensions",
    "debug_toolbar",
]  # noqa F405
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#middleware
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa F405
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

def _custom_show_toolbar(request) -> bool:
    """Only show the debug toolbar to users with the superuser flag."""
    return DEBUG and request.user.is_superuser

# https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-config
DEBUG_TOOLBAR_CONFIG: dict = {
    'SHOW_TOOLBAR_CALLBACK': '{{ cookiecutter.project_base }}.settings.local._custom_show_toolbar',
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
}
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
INTERNAL_IPS: list[str] = ["127.0.0.1", "10.0.2.2"]

# ==============================
# django-extensions
# ==============================
SHELL_PLUS = "ipython"


