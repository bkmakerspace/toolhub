from environ import Env

from .base import *  # noqa: F401, F403

env = Env()

DEBUG = False

SECRET_KEY = env.str("DJANGO_SECRET_KEY", default="!!!SET DJANGO_SECRET_KEY!!!")

TEST_RUNNER = 'utils.test_runner.PytestTestRunner'

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test.sql',
    }
}

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
EMAIL_HOST = "localhost"
EMAIL_PORT = 1025
