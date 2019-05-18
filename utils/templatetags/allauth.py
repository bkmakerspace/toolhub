from allauth.socialaccount import providers
from allauth.socialaccount.templatetags.socialaccount import ProvidersMediaJSNode, get_providers
from allauth.utils import get_request_param
from django_jinja import library
from jinja2.utils import contextfunction
from jinja2 import is_undefined


@library.global_function
def get_social_providers():
    return get_providers()


@library.global_function
@contextfunction
def provider_login_url(context, provider, **params):
    # return ProviderLoginURLNode(provider_id, params).render(context)

    request = context["request"]
    if isinstance(provider, str):
        provider = providers.registry.by_id(provider, request)
    auth_params = params.get("auth_params", None)
    scope = params.get("scope", None)
    process = params.get("process", None)
    if is_undefined(scope):
        del params["scope"]
    if is_undefined(auth_params):
        del params["auth_params"]
    if "next" not in params:
        next_url = get_request_param(request, "next")
        if next_url:
            params["next"] = next_url
        elif process == "redirect":
            params["next"] = request.get_full_path()
    else:
        if not params["next"]:
            del params["next"]
    # get the login url and append params as url parameters
    return provider.get_login_url(request, **params)


@library.global_function
@contextfunction
def providers_media_js(context):
    return ProvidersMediaJSNode().render(context)
