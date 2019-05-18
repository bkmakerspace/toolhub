from braces.views import SelectRelatedMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import login as auth_login
from django.views.generic import CreateView, DetailView, UpdateView
from django.urls import reverse_lazy

from toolhub import toolhub_settings
from tools.models import UserTool
from utils.mixins import RestrictToUserMixin

from .forms import AuthenticationForm, SignupForm, UserProfileUpdateForm
from .models import User, UserProfile


class ToolhubLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = "auth/login.jinja"
    redirect_authenticated_user = True

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form and set return status to 401"""
        return self.render_to_response(self.get_context_data(form=form), status=401)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["use_password"] = toolhub_settings["auth"]["use_password_auth"]
        return ctx


class SignupView(CreateView):
    form_class = SignupForm
    template_name = "auth/signup.jinja"
    redirect_authenticated_user = True
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        response = super().form_valid(form)
        auth_login(self.request, user=self.object)
        return response


class ProfileView(LoginRequiredMixin, SelectRelatedMixin, DetailView):
    model = User
    template_name = "auth/profile.jinja"
    context_object_name = "profile_user"
    select_related = ("profile",)

    def get_context_data(self, **kwargs):
        if self.extra_context is None:
            self.extra_context = {}
        self.extra_context.update(
            {
                "borrowing": UserTool.objects.visible_to_user(self.request.user)
                .borrowing_by_user(self.object)
                .order_by("-last_history_date")
            }
        )
        return super().get_context_data(**kwargs)


class EditProfileView(RestrictToUserMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileUpdateForm
    template_name = "auth/profile_update.jinja"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_success_url(self):
        return self.object.get_absolute_url()
