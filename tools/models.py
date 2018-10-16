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
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel, TitleDescriptionModel
from tagulous.models import TagField, TagTreeModel

from utils.models import StateMachineMixin

from .querysets import ToolHistoryQuerySet, UserToolQuerySet


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

    class TagMeta:
        force_lowercase = False
        space_delimiter = False


class ToolStates(Catalog):
    _attrs = "value", "label", "availability_label", "badge_type"
    none = "none", _("None"), None, None
    unused = "unused", _("Unused"), _("Available"), "success"
    loaned = "loaned", _("Loaned"), _("In Use"), "warning"
    disabled = "disabled", _("Decommissioned"), _("Retired"), "danger"


class ToolTransitions(Catalog):
    _attrs = "value", "label", "source", "dest"
    create = 0, _("Create"), ToolStates.none.value, ToolStates.unused.value
    borrow = 1, _("Borrow"), ToolStates.unused.value, ToolStates.loaned.value
    return_ = 2, _("Return"), ToolStates.loaned.value, ToolStates.unused.value
    decommission = 3, _("Decommission"), "*", ToolStates.disabled.value
    reinstate = 4, _("Reinstate"), ToolStates.disabled.value, ToolStates.unused.value


class ToolVisibility(Catalog):
    _attrs = "value", "label"
    private = 0, _("Visible to owner")
    cleared = 1, _("Visible to cleared")
    public = 2, _("Visbile to everyone")


class ToolClearance(Catalog):
    _attrs = "value", "label"
    none = 0, _("No clearance")
    owner = 1, _("Owner approved")
    cleared = 2, _("Cleared-user approved")


class UserTool(StateMachineMixin, TitleDescriptionModel, TimeStampedModel):
    """A tool owned by a User"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="tools"
    )
    description = models.TextField(blank=True)
    state = models.CharField(
        max_length=10,
        choices=ToolStates._zip("value", "label"),
        default=ToolStates.none.value,
        editable=False,
    )
    taxonomies = TagField(to=ToolTaxonomy, blank=True, related_name="tools")
    visibility = models.PositiveSmallIntegerField(
        _("Visibility"),
        choices=ToolVisibility._zip("value", "label"),
        default=ToolVisibility.public.value,
    )
    clearance = models.PositiveSmallIntegerField(
        _("Clearance"),
        choices=ToolClearance._zip("value", "label"),
        default=ToolClearance.none.value,
    )

    objects = UserToolQuerySet.as_manager()

    class StateMachine:
        auto_transitions = False
        send_event = True
        states = [{"name": state.value} for state in ToolStates]
        transitions = [
            {"trigger": trigger, "source": source, "dest": dest}
            for trigger, source, dest in ToolTransitions._zip("name", "source", "dest")
        ]
        after_state_change = "record_transition"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tools:detail', kwargs={'pk': self.pk})

    def record_transition(self, event):
        if not event.kwargs.get("skip_save", False):
            self.save()
        self.history.create(
            user=event.kwargs.get("user"),
            action=ToolTransitions(event.event.name, "name").value,
        )

    class Meta:
        ordering = ("-created",)
        get_latest_by = "created"
        verbose_name = _("Tool")
        verbose_name_plural = _("Tools")


class ToolHistory(TimeStampedModel):
    tool = models.ForeignKey(UserTool, on_delete=models.CASCADE, related_name="history")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="tool_history",
    )
    action = models.PositiveSmallIntegerField(
        choices=ToolTransitions._zip("value", "label")
    )

    objects = ToolHistoryQuerySet.as_manager()

    def __str__(self):
        action = ToolTransitions(self.action).label
        return f"{self.tool} - {action}"

    class Meta:
        ordering = ("-created",)
        get_latest_by = "created"
        verbose_name = _("Tool History")
        verbose_name_plural = _("Tool Histories")


class ClearancePermission(TimeStampedModel):
    tool = models.ForeignKey(
        UserTool, on_delete=models.CASCADE, related_name="permissions"
    )
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

    def __str__(self):
        return f"{self.cleared_by_user} cleared {self.cleared_user} ({self.tool})"


class ToolPhoto(TimeStampedModel):
    tool = models.ForeignKey(UserTool, on_delete=models.CASCADE, related_name="photos")
    uploading_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="uploaded_photos",
    )
    file = models.FileField()
    title = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ("-created",)
        get_latest_by = "created"
