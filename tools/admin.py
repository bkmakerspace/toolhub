import logging

from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
import tagulous.admin
from tagulous import forms as tag_forms

from .models import ClearancePermission, ToolHistory, ToolTaxonomy, ToolPhoto, UserTool


logger = logging.getLogger(__name__)


# temporary monkey patch until pr is merged
# https://github.com/radiac/django-tagulous/pull/58
render_super = tag_forms.TagWidgetBase.render


def replaced_render(self, name, value, attrs={}, renderer=None):
    return render_super(self, name, value, attrs=attrs)


tag_forms.TagWidgetBase.render = replaced_render


class UserToolAdmin(MarkdownxModelAdmin):
    list_display = ("title", "user", "taxonomies", "visibility", "clearance")
    list_select_related = ("user",)
    list_filter = ("state", "visibility", "clearance")
    raw_id_fields = ("user",)


class ToolTaxonomyAdmin(tagulous.admin.TagModelAdmin):
    list_display = ("name", "count", "protected", "state", "color")
    list_filter = ("protected", "state")
    exclude = ("count",)
    actions = ("merge_tags",)


@admin.register(ClearancePermission)
class ClearancePermissionAdmin(admin.ModelAdmin):
    list_display = ("__str__", "created")
    raw_id_fields = ("tool", "cleared_by_user", "cleared_user")


@admin.register(ToolHistory)
class ToolHistoryAdmin(admin.ModelAdmin):
    date_hierarchy = "created"
    list_display = ("tool", "action", "user", "created")
    list_filter = ("action",)
    raw_id_fields = ("user",)


@admin.register(ToolPhoto)
class ToolPhotoAdmin(admin.ModelAdmin):
    date_hierarchy = "created"
    raw_id_fields = ("tool", "uploading_user")


tagulous.admin.register(ToolTaxonomy, ToolTaxonomyAdmin)
tagulous.admin.register(UserTool, UserToolAdmin)


__all__ = []
