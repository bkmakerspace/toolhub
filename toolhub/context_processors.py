from django.conf import settings as dj_settings


def settings(request):
    # There's a pretty big security risk to simply exposing all settings to templates.
    # For this reason, only expose settings that are absolutely needed.
    # NEVER include settings that contain credentials or other secrets.
    return {
        'DEFAULT_PAGINATE_BY': dj_settings.DEFAULT_PAGINATE_BY,
        'SHORT_PAGINATE_BY': dj_settings.SHORT_PAGINATE_BY,
    }
