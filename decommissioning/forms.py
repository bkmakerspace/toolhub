from crispy_forms.layout import Submit
from django import forms
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from utils.forms import CrispyFormMixin


class DecommissionForm(CrispyFormMixin, forms.Form):
    has_columns = False

    def get_form_action(self):
        tool = self.initial.get("tool")
        return reverse("decommissioning:decommission", kwargs=dict(pk=tool.pk))

    def layout_args(self, helper):
        return (Submit("decommission", _("Decommission Tool"),css_class="btn-danger"),)


class ReinstateForm(CrispyFormMixin, forms.Form):
    def get_form_action(self):
        tool = self.initial.get("tool")
        return reverse("decommissioning:reinstate", kwargs=dict(pk=tool.pk))

    def layout_args(self, helper):
        return (Submit("reinstate", _("Reinstate Tool")),)
