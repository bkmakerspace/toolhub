from crispy_forms.layout import Field, Submit
from django import forms
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

# from tools.models import UserTool
# from toolhub_auth.models import User
from utils.forms import CrispyFormMixin


class BorrowForm(CrispyFormMixin, forms.Form):
    def get_form_action(self):
        tool = self.initial.get("tool")
        return reverse("borrowing:borrow", kwargs=dict(pk=tool.pk))

    def layout_args(self, helper):
        return (Submit("borrow", _("Borrow Tool")),)


class ReturnForm(CrispyFormMixin, forms.Form):
    def get_form_action(self):
        tool = self.initial.get("tool")
        return reverse("borrowing:return", kwargs=dict(pk=tool.pk))

    def layout_args(self, helper):
        return (Submit("return", _("Return Tool")),)
