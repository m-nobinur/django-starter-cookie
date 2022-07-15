from .base import *  # noqa

TEST_RUNNER = "django.test.runner.DiscoverRunner"

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
