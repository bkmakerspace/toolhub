from django.conf import settings

from utils import deep_update


default_app_config = "toolhub.apps.ToolhubConfig"


def get_settings():
    defaults = {
        'auth': {
            'use_allauth': False,
            'slack': {
                'required_group': None,
            },
        },
        'messages': {
            'non_member': 'You must be a member of the space to access Toolhub',
        },
    }
    return deep_update(defaults, getattr(settings, 'TOOLHUB', {}))


toolhub_settings = get_settings()
