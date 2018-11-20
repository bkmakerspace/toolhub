from environ import Env

from .base import *  # noqa: F401, F403

env = Env()


SECRET_KEY = env.str("SECRET_KEY", default="keepitsecret")
DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])
INTERNAL_IPS = env.list("INTERNAL_IPS", default=["172.21.0.1"])
DATABASES = {"default": env.db(default="sqlite:///db.sqlite")}
TIME_ZONE = env.str("TIME_ZONE", default="UTC")
LANGUAGE_CODE = env.str("LANGUAGE_CODE", default="en-us")

STATIC_ROOT = env.str("STATIC_ROOT", default=f"{BASE_DIR}static/")  # noqa: F405
STATIC_URL = env.str("STATIC_URL", default="/static/")
MEDIA_ROOT = env.str("MEDIA_ROOT", default=f"{BASE_DIR}media/")  # noqa: F405
MEDIA_URL = env.str("MEDIA_URL", default="/media/")

ELASTICSEARCH_DSL = {
    "default": {
        "hosts": [env.str("SEARCH_HOST")],
    }
}
