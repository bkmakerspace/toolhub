from braces.forms import UserKwargModelFormMixin
from crispy_forms.layout import Button, Div, Field, Fieldset, Reset, Submit
from django import forms
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from toolhub_auth.models import User
from tools.models import ClearancePermission, ToolPhoto, UserTool
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
                # attempts
                # css_class="h-100", label_class="", field_class="", help_text="test"
                Field("description"),
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

    def post_super_init(self):
        super().post_super_init()
        self.update_markdown_upload_path()

    def update_markdown_upload_path(self):
        if hasattr(self, "instance") and self.pk_field:
            reverse_kwargs = {self.pk_field: self.instance.pk}
        else:
            reverse_kwargs = {}
        attrs = self.fields["description"].widget.attrs
        attrs.update(
            {
                "data-markdownx-upload-urls-path": reverse(
                    "tools:upload_tool_photo", kwargs=reverse_kwargs
                )
            }
        )


class UserToolUpdateForm(UserToolCreateForm):
    action_button_label = _("Update tool")
    form_action = "tools:edit"
    pk_field = "pk"


class UserToolFilterViewForm(CrispyFormMixin, forms.Form):
    has_columns = False

    def layout_args(self, helper):
        helper.form_method = "GET"
        return (
            Fieldset("", Field("name"), Field("state"), Field("taxonomies")),
            Div(
                Submit("action", _("Filter"), css_class="btn-success"),
                Button(
                    "advanced",
                    _("Advanced"),
                    css_class="btn-primary",
                    data_toggle="collapse",
                    data_target="#advancedFilters",
                ),
                Reset("clear", _("Clear"), css_class="btn-danger"),
                css_class="btn-group",
            ),
            Fieldset(
                "",
                Field("user"),
                Field("borrower"),
                css_id="advancedFilters",
                css_class="collapse",
            ),
        )

    def clean(self):
        if any([self.cleaned_data["user"], self.cleaned_data["borrower"]]):
            self.helper.layout.fields[2].css_class += " show"
        return super().clean()


class ClearancePermissionForm(CrispyFormMixin, forms.Form):
    cleared_users = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(), widget=forms.CheckboxSelectMultiple()
    )

    def __init__(self, *args, instance=None, cleared_by_user=None, **kwargs):
        self.instance = instance
        self.cleared_by_user = cleared_by_user

        super().__init__(*args, **kwargs)

        self.initial = {"cleared_users": self._init_users}
        self.fields["cleared_users"].queryset = User.objects.exclude(
            pk=self.instance.user.pk
        ).filter(is_active=True)

    def layout_args(self, helper):
        return (
            Field("cleared_users"),
            Submit("action", _("Update Clearance"), css_class="offset-md-3"),
        )

    def _init_users(self):
        return self.instance.permissions.values_list("cleared_user", flat=True)

    def save(self):
        init_users = set(self._init_users())
        edited_users = set(self.cleaned_data["cleared_users"].values_list("pk", flat=True))
        added_users = edited_users - init_users
        ClearancePermission.objects.bulk_create(
            [
                ClearancePermission(
                    tool=self.instance,
                    cleared_user_id=user_id,
                    cleared_by_user=self.cleared_by_user,
                )
                for user_id in added_users
            ]
        )
        removed_users = init_users - edited_users
        self.instance.permissions.filter(cleared_user_id__in=removed_users).delete()


class UploadToolPhotoForm(UserKwargModelFormMixin, forms.ModelForm):
    """
    Optionally takes a tool to make association
    Also set the `uploading_user`?
    """

    class Meta:
        model = ToolPhoto
        fields = ("file",)

    def __init__(self, *args, **kwargs):
        # move file uploaded to what the form expects
        kwargs["files"]["file"] = kwargs["files"]["image"]
        self.tool = kwargs.pop("tool", None)
        return super().__init__(*args, **kwargs)

    def save(self, commit=True):
        # This will set the photo tool to null if none was passed
        self.instance.tool = self.tool
        self.instance.uploading_user = self.user
        # NOTE: get title from file name temporarily
        return super().save(commit=commit)
