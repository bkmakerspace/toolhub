from crispy_forms.layout import Button, Layout, Fieldset, Submit, Field, Div
from django import forms
from django.utils.translation import ugettext_lazy as _

from tools.models import UserTool
from utils.forms import CrispyFormMixin


class UserToolCreateForm(CrispyFormMixin, forms.ModelForm):
    action_button_label = _("Add tool")
    form_action = "tools:create"

    def __init__(self, *args, **kwargs):
        super(UserToolCreateForm, self).__init__(cols=(2, 10), *args, **kwargs)

    def layout_args(self, helper):
        return (
            Fieldset(
                None,
                Field("title"),
                Field("description", css_class="h-100", label_class="", field_class=""),
                Field("taxonomies"),
                Field("visibility"),
                Field("clearance"),
            ),
            Div(
                Div(Submit("action", self.action_button_label), css_class="offset-md-2"),
                css_class="form-group",
            ),
        )

    class Meta:
        fields = ("title", "description", "taxonomies", "visibility", "clearance")
        model = UserTool


class UserToolUpdateForm(UserToolCreateForm):
    action_button_label = _("Update tool")
    form_action = "tools:edit"
    pk_field = "pk"


class UserToolFilterViewForm(CrispyFormMixin, forms.Form):
    has_columns = False

    def layout_args(self, helper):
        helper.form_method = "GET"
        return (
            Field("name"),
            Field("taxonomies"),
            Submit("action", _("Filter")),
            # Button('clear', _("Clear Filter"), type="reset")
        )
