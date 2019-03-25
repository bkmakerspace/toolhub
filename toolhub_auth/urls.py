from django.conf import settings
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


if toolhub_settings['auth']['use_allauth']:
    urlpatterns = [path("accounts/", include("allauth.urls"))]
else:
    urlpatterns = [
        path("signup/", SignupView.as_view(), name="account_signup"),
        path("login/", ToolhubLoginView.as_view(), name="account_login"),
        path("logout/", LogoutView.as_view(), name="account_logout"),
        path("password/change/", PasswordChangeView.as_view(), name="account_change_password"),
        path("password/change/done/", PasswordChangeDoneView.as_view(), name="account_change_password_done"),
        path("password/reset/", PasswordResetView.as_view(), name="account_reset_password"),
        path("password/reset/done/", PasswordResetDoneView.as_view(), name="account_reset_password_done"),
        path(
            "password/reset/confirm/<uidb64>/<token>/",
            PasswordResetConfirmView.as_view(),
            name="account_reset_password_from_key",
        ),
        path(
            "password/reset/complete/",
            PasswordResetCompleteView.as_view(),
            name="account_reset_password_from_key_done",
        ),
    ]


urlpatterns += [
    path("profile/<int:pk>", ProfileView.as_view(), name="profile"),
    path("profile/update/", EditProfileView.as_view(), name="update_profile"),
]
