from crispy_forms.layout import Layout, Fieldset, Submit, Field, Div, HTML
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm as DjangoAuthenticationForm,
    # UserCreationForm as DjangoUserCreationForm,
)
from django.utils.translation import ugettext_lazy as _
from utils.forms import CrispyFormMixin, FormActions


class AuthenticationForm(CrispyFormMixin, DjangoAuthenticationForm):

    has_columns = False

    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Field("username"),
            Field("password"),
            Div(
                Div(
                    Submit(None, "Login"),
                    HTML(
                        '<a class="btn btn-secondary ml-auto" href="{% url \'password_reset\' %}">Forgot Password?</a>'
                    ),
                    css_class="d-flex",
                ),
                css_class="form-group mb-0",
            ),
        )


class SignupForm(CrispyFormMixin, forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    has_columns = False

    class Meta:
        model = get_user_model()
        fields = ("email", "first_name", "last_name")

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Div(
                Fieldset(
                    "Account details",
                    Field("email"),
                    Field("password1"),
                    css_class="col-md-6",
                ),
                Fieldset(
                    "Extra Information",
                    Field("first_name"),
                    Field("last_name"),
                    css_class="col-md-6",
                ),
                FormActions(Submit("signup", _("Sign up")), css_class="col-12 mb-0"),
                css_class="row",
            )
        )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        User = get_user_model()
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("There is already a user with that email.")
        return email
