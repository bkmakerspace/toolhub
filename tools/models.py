"""
Tools are singular physical objects or process grouped physical
objects that are used to perform a specific task

they have multiple taxonomies
Process, what sorta processes this tool can be used for
Automation, what level of automation this tool contains for accomplishing the process?
Approach,
Viewpoint
"""
from catalog import Catalog
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TitleDescriptionModel, TimeStampedModel
from django_extensions.db.fields import AutoSlugField
from tagulous.models import TagTreeModel, TagField


class ToolTaxonomy(TagTreeModel):
    """A generic way of describing a tool, the top level is the base taxonomy"""

    # order = models.IntegerField(blank=False, default=0)

    # Published state
    # Allows users to submit new taxonomies that are evaluated and approved
    class State(Catalog):
        _attrs = "value", "label"
        in_review = 0, _("in review")
        approved = 1, _("approved")
        rejected = 2, _("rejected")

    state = models.PositiveSmallIntegerField(
        _("State"), choices=State._zip("value", "label"), default=State.in_review.value
    )

    class Meta:
        verbose_name = _("Tool Taxonomy")
        verbose_name_plural = _("Tool Taxonomies")

    # class TagMeta:
    #     force_lowercase = True


class UserTool(TitleDescriptionModel, TimeStampedModel):
    """A tool owned by a User"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    description = models.TextField(blank=True)

    taxonomoies = TagField(to=ToolTaxonomy, blank=True, related_name="tools")

    class Clearance(Catalog):
        _attrs = "value", "label"
        none = None, _("No clearance")
        private = 0, _("Private tool")
        public = 1, _("Public tool")
        owner_approved = 2, _("Owner approved")

    clearance = models.PositiveSmallIntegerField(
        _("Clearance"),
        choices=Clearance._zip("value", "label"),
        default=Clearance.private.value,
    )


# class ToolHistory(TimeStampedModel):
#     # Actions Catalog
#     class Actions(Catalog):
#         _attrs = "value", "label"
#     tool = models.ForeignKey(UserTool, on_delete=models.CASCADE)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)


class ClearancePermission(TimeStampedModel):
    tool = models.ForeignKey(UserTool, on_delete=models.CASCADE)
    cleared_by_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="given_tool_permissions",
    )
    cleared_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="tool_permissions",
    )


class ToolPhoto(TimeStampedModel):
    tool = models.ForeignKey(UserTool, on_delete=models.CASCADE)
    uploading_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT
    )
    file = models.FileField()
    title = models.CharField(max_length=255, blank=True)
