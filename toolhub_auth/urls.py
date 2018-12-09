from django.contrib.auth.views import (
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.urls import path

from toolhub_auth.views import ToolhubLoginView, SignupView, ProfileView


urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", ToolhubLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password/change/", PasswordChangeView.as_view(), name="password_change"),
    path("password/change/done/", PasswordChangeDoneView.as_view(), name="password_change_done"),
    path("password/reset/", PasswordResetView.as_view(), name="password_reset"),
    path("password/reset/done/", PasswordResetDoneView.as_view(), name="password_reset_done"),
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
]
