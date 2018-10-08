from django.contrib.auth.views import LoginView
from django.contrib.auth import login as auth_login
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import AuthenticationForm, SignupForm


class ToolhubLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = "auth/login.jinja"
    redirect_authenticated_user = True


class SignupView(CreateView):
    form_class = SignupForm
    template_name = "auth/signup.jinja"
    redirect_authenticated_user = True
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        response = super().form_valid(form)
        auth_login(self.request, user=self.object)
        return response
