from django.conf import settings
from django.apps import AppConfig


class ToolhubConfig(AppConfig):
    name = "toolhub"

    def ready(self):
        from django.contrib.flatpages import views as flatpages_views

        flatpages_views.DEFAULT_TEMPLATE = getattr(
            settings, "DEFAULT_FLATPAGES_TEMPLATE", "flatpages/default.jinja"
        )
