import os

from django.contrib.messages import constants as message_constants
from django.urls import reverse_lazy

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SECRET_KEY = "wataboutthechildren"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.forms",
    "django_extensions",
    "django_jinja.contrib._humanize",
    "tagulous",
    "crispy_forms",
    "django_filters",
    "colorful",
    "debug_toolbar",
    "qr_code",
    "toolhub",
    "toolhub_auth.apps.ToolhubAuthConfig",
    "tools.apps.ToolsConfig",
    "borrowing.apps.BorrowingConfig",
    "utils",
    "markdownx",  # placed below all so templates can be overwritten
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

INTERNAL_IPS = ["127.0.0.1"]

ROOT_URLCONF = "toolhub.urls"

LOGIN_URL = reverse_lazy("login")
LOGIN_REDIRECT_URL = reverse_lazy("tools:home")
LOGOUT_REDIRECT_URL = reverse_lazy("home")

TEMPLATES = [
    {
        "BACKEND": "django_jinja.backend.Jinja2",
        "APP_DIRS": True,
        "OPTIONS": {
            "match_extension": ".jinja",
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "extensions": [
                "jinja2.ext.do",
                "jinja2.ext.loopcontrols",
                "jinja2.ext.with_",
                "jinja2.ext.i18n",
                "jinja2.ext.autoescape",
                "django_jinja.builtins.extensions.CsrfExtension",
                "django_jinja.builtins.extensions.CacheExtension",
                "django_jinja.builtins.extensions.TimezoneExtension",
                "django_jinja.builtins.extensions.UrlsExtension",
                "django_jinja.builtins.extensions.StaticFilesExtension",
                "django_jinja.builtins.extensions.DjangoFiltersExtension",
                "tools.extensions.ToolConstantsExtension",
            ],
            "auto_reload": True,
            "autoescape": True,
            "keep_trailing_newline": True,
            "lstrip_blocks": True,
            "trim_blocks": True,
        },
    },
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    },
]

# Use above template engines when choosing form renderer
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

AUTH_USER_MODEL = "toolhub_auth.User"

WSGI_APPLICATION = "toolhub.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


USE_I18N = True
USE_L10N = True
USE_TZ = True

CRISPY_TEMPLATE_PACK = "bootstrap4"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DEFAULT_PAGINATE_BY = 18

MESSAGE_TAGS = {
    message_constants.DEBUG: "alert-dark",
    message_constants.INFO: "alert-info",
    message_constants.SUCCESS: "alert-success",
    message_constants.WARNING: "alert-warning",
    message_constants.ERROR: "alert-danger",
}

# MarkdownX settings
MARKDOWNX_MARKDOWN_EXTENSIONS = [
    "markdown.extensions.extra",
    "markdown.extensions.abbr",
    "markdown.extensions.attr_list",
    "markdown.extensions.def_list",
    "markdown.extensions.fenced_code",
    "markdown.extensions.footnotes",
    "markdown.extensions.tables",
    "markdown.extensions.admonition",
    "markdown.extensions.codehilite",
    "markdown.extensions.meta",
    "markdown.extensions.nl2br",
    "markdown.extensions.sane_lists",
    "markdown.extensions.smarty",
    "markdown.extensions.toc",
    "markdown.extensions.wikilinks",
]
