from crispy_forms.layout import Fieldset, Submit, Field, Div, HTML
from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import AuthenticationForm as DjangoAuthenticationForm
from django.utils.translation import ugettext_lazy as _
from utils.forms import CrispyFormMixin, FormActions


class AuthenticationForm(CrispyFormMixin, DjangoAuthenticationForm):

    has_columns = False

    def layout_args(self, helper):
        return (
            Fieldset(_("Login"), Field("username"), Field("password")),
            Div(
                Div(
                    Submit(None, "Login"),
                    HTML(
                        '<a class="btn btn-secondary ml-auto" '
                        "href=\"{% url 'password_reset' %}\">Forgot Password?</a>"
                    ),
                    css_class="d-flex",
                ),
                css_class="form-group mb-0",
            ),
        )


class SignupForm(CrispyFormMixin, forms.ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        help_text=password_validation.password_validators_help_text_html(),
    )

    has_columns = False

    class Meta:
        model = get_user_model()
        fields = ("email", "first_name", "last_name")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({'autofocus': True})

    def layout_args(self, helper):
        return (
            Div(
                Fieldset(
                    _("New account details"),
                    Field("email"),
                    Field("password"),
                    css_class="col-md-6",
                ),
                Fieldset(
                    _("Extra Information"),
                    Field("first_name"),
                    Field("last_name"),
                    css_class="col-md-6",
                ),
                FormActions(Submit("signup", _("Sign up")), css_class="col-12 mb-0"),
                css_class="row",
            ),
        )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        User = get_user_model()
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("There is already a user with that email.")
        return email

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get("password")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error("password", error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
