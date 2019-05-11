import requests
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from allauth.exceptions import ImmediateHttpResponse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.utils.translation import ugettext_lazy as _

from toolhub import toolhub_settings


class ToolhubSocialAccountAdapter(DefaultSocialAccountAdapter):
    groups_url = 'https://slack.com/api/groups.list'

    def pre_social_login(self, request, sociallogin):
        if (sociallogin.account.provider == 'slack' and
                toolhub_settings['auth']['slack']['required_group']):
            resp = requests.get(
                self.groups_url,
                params={'token': sociallogin.token}
            )
            resp = resp.json()
            if not resp.get('ok'):
                raise OAuth2Error()

            group_names = [g['name'] for g in resp['groups']]
            if toolhub_settings['auth']['slack']['required_group'] not in group_names:
                messages.error(request, _(toolhub_settings['messages']['non_member']))
                raise ImmediateHttpResponse(HttpResponseRedirect(reverse('account_login')))
