from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FlatPagesConfig(AppConfig):
    name = "toolhub.contrib.toolhub_flatpages"
    verbose_name = _("Flat Pages")
