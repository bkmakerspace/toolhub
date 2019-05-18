from importlib import import_module

from django.contrib.auth.views import (
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.urls import path, include

from toolhub import toolhub_settings
from toolhub_auth.views import EditProfileView, ToolhubLoginView, SignupView, ProfileView


# if toolhub_settings['auth']['use_allauth']:
# urlpatterns = []
# else:
urlpatterns = [
    # path("accounts/", include("allauth.urls")),
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", ToolhubLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password/change/", PasswordChangeView.as_view(), name="password_change"),
    path(
        "password/change/done/",
        PasswordChangeDoneView.as_view(),
        name="password_change_done"
    ),
    path("password/reset/", PasswordResetView.as_view(), name="password_reset"),
    path(
        "password/reset/done/",
        PasswordResetDoneView.as_view(),
        name="password_reset_done"
    ),
    path(
        "password/reset/confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password/reset/complete/",
        PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path("profile/<int:pk>", ProfileView.as_view(), name="profile"),
    path("profile/update/", EditProfileView.as_view(), name="update_profile"),
]

if toolhub_settings['auth']['use_allauth']:
    from allauth.socialaccount import providers
    for provider in providers.registry.get_list():
        try:
            prov_mod = import_module(provider.get_package() + '.urls')
        except ImportError:
            continue
        prov_urlpatterns = getattr(prov_mod, 'urlpatterns', None)
        if prov_urlpatterns:
            urlpatterns += prov_urlpatterns
