from utils.env import Env

from .base import *  # noqa: F401, F403

env = Env()


SECRET_KEY = env.str("SECRET_KEY", default="keepitsecret")
DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])
INTERNAL_IPS = env.list("INTERNAL_IPS", default=["172.21.0.1"])
DATABASES = {"default": env.db(default="sqlite:///db.sqlite")}
TIME_ZONE = env.str("TIME_ZONE", default="UTC")
LANGUAGE_CODE = env.str("LANGUAGE_CODE", default="en-us")

STATIC_ROOT = env.str("STATIC_ROOT", default=f"{BASE_DIR}/static/")  # noqa: F405
STATIC_URL = env.str("STATIC_URL", default="/static/")
MEDIA_ROOT = env.str("MEDIA_ROOT", default=f"{BASE_DIR}/media/")  # noqa: F405
MEDIA_URL = env.str("MEDIA_URL", default="/media/")

EMAIL_BACKEND = env.str("EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")

if env.bool("DEBUG_TOOLBAR_ENABLE", default=False):
    INSTALLED_APPS += ["debug_toolbar"]  # noqa: F405
    MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE  # noqa: F405

TOOLHUB = env.eval("TOOLHUB", default={})

if TOOLHUB.get("auth", {}).get("use_allauth", False):
    AUTHENTICATION_BACKENDS += (  # noqa: F405
        "allauth.account.auth_backends.AuthenticationBackend",
    )
    INSTALLED_APPS += [provider for provider in env.list("ALLAUTH_PROVIDERS")]
    ACCOUNT_AUTHENTICATION_METHOD = "email"
    ACCOUNT_EMAIL_REQUIRED = True
    ACCOUNT_EMAIL_VERIFICATION = "none"
    ACCOUNT_USER_MODEL_USERNAME_FIELD = None
    ACCOUNT_USERNAME_REQUIRED = False
    SOCIALACCOUNT_ADAPTER = "utils.auth.ToolhubSocialAccountAdapter"
    ACCOUNT_LOGOUT_ON_GET = True
    ACCOUNT_TEMPLATE_EXTENSION = "jinja"
