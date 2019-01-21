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
from colorful.fields import RGBColorField
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel, TitleDescriptionModel
from markdownx.models import MarkdownxField
from tagulous.models import TagField, TagTreeModel

from utils.models import StateMachineMixin

from tools.exceptions import ToolAvailabilityException, ToolClearanceException
from tools.querysets import ToolHistoryQuerySet, UserToolQuerySet


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

    color = RGBColorField(null=True)

    class Meta:
        verbose_name = _("Tool Taxonomy")
        verbose_name_plural = _("Tool Taxonomies")

    class TagMeta:
        force_lowercase = False
        space_delimiter = False

    def get_color(self):
        if not self.color and self.parent:
            # try to get color from parent (this can cascade)
            return self.parent.get_color()
        else:
            return self.color

    def get_absolute_url(self):
        return reverse("tools:taxonomy_detail", kwargs={"path": self.path})


class ToolStates(Catalog):
    _attrs = "value", "label", "badge_type"
    none = "none", _("None"), None
    available = "available", _("Available"), "success"
    in_use = "in_use", _("In Use"), "warning"
    disabled = "disabled", _("Disabled"), "danger"


class ToolTransitions(Catalog):
    _attrs = "value", "label", "source", "dest"
    create = 0, _("Create"), ToolStates.none.value, ToolStates.available.value
    borrow = 1, _("Borrow"), ToolStates.available.value, ToolStates.in_use.value
    return_ = 2, _("Return"), ToolStates.in_use.value, ToolStates.available.value
    decommission = 3, _("Decommission"), "*", ToolStates.disabled.value
    reinstate = 4, _("Reinstate"), ToolStates.disabled.value, ToolStates.available.value


class UserTool(StateMachineMixin, TitleDescriptionModel, TimeStampedModel):
    """A tool owned by a User"""

    States = ToolStates

    Transitions = ToolTransitions

    class Visibility(Catalog):
        _attrs = "value", "label", "card_class"
        private = 0, _("Private"), "border-warning"
        cleared = 1, _("Cleared Users"), "border-success"
        public = 2, _("Public"), None

    class Clearance(Catalog):
        _attrs = "value", "label"
        none = 0, _("Available to all")
        owner = 1, _("Owner cleared users only")
        cleared = 2, _("Cleared users can approve anyone")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="tools"
    )
    description = MarkdownxField(blank=True)
    state = models.CharField(
        max_length=10,
        choices=States._zip("value", "label"),
        default=States.none.value,
        editable=False,
    )
    taxonomies = TagField(to=ToolTaxonomy, blank=True, related_name="tools")
    visibility = models.PositiveSmallIntegerField(
        _("Visibility"),
        choices=Visibility._zip("value", "label"),
        default=Visibility.public.value,
        help_text=_("The level of user visibility for this tool"),
    )
    clearance = models.PositiveSmallIntegerField(
        _("Clearance"),
        choices=Clearance._zip("value", "label"),
        default=Clearance.none.value,
        help_text=_("Who is allowed to clear a user to use this tool"),
    )

    objects = UserToolQuerySet.as_manager()

    class Meta:
        ordering = ("-created",)
        get_latest_by = "created"
        verbose_name = _("Tool")
        verbose_name_plural = _("Tools")

    class StateMachine(StateMachineMixin.StateMachine):
        states = [{"name": state.value} for state in ToolStates]
        transitions = [
            {"trigger": trigger, "source": source, "dest": dest}
            for trigger, source, dest in ToolTransitions._zip("name", "source", "dest")
        ]
        after_state_change = "record_transition"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("tools:detail", kwargs={"pk": self.pk})

    def record_transition(self, event):
        if not event.kwargs.get("skip_save", False):
            self.save()
        self.history.create(
            user=event.kwargs.get("user"), action=self.Transitions(event.event.name, "name").value
        )

    def check_clearance(self, user):
        return self.permissions.filter(cleared_user=user).exists()

    def user_can_grant_clearance(self, user):
        """See if we're allowed to grant clearance"""
        level = self.Clearance(self.clearance)
        if level == self.Clearance.none:
            return True
        if level == self.Clearance.owner:
            return self.user == user
        if level == self.Clearance.cleared:
            return self.user == user or self.check_clearance(user)

    def user_can_borrow(self, user):
        return self._meta.model.objects.borrowable_to_user(user).filter(pk=self.pk).exists()

    def prepare_borrow(self, event):
        """Do validation before allowing a user to borrow a tool"""
        user = event.kwargs.get("user")
        if not self.user_can_borrow(user):
            raise ToolClearanceException("%s isn't allowed to borrow this tool" % user)
        # Is this needed?
        if not self.is_available():
            raise ToolAvailabilityException()


class ToolHistory(TimeStampedModel):
    tool = models.ForeignKey(UserTool, on_delete=models.CASCADE, related_name="history")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="tool_history",
    )
    action = models.PositiveSmallIntegerField(choices=UserTool.Transitions._zip("value", "label"))

    objects = ToolHistoryQuerySet.as_manager()

    class Meta:
        ordering = ("-created",)
        get_latest_by = "created"
        verbose_name = _("Tool History")
        verbose_name_plural = _("Tool Histories")

    def __str__(self):
        action = UserTool.Transitions(self.action).label
        return f"{self.tool} - {action}"


class ClearancePermission(TimeStampedModel):
    tool = models.ForeignKey(UserTool, on_delete=models.CASCADE, related_name="permissions")
    cleared_by_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="given_tool_permissions"
    )
    cleared_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="tool_permissions"
    )

    class Meta:
        ordering = ("-created",)
        get_latest_by = "created"
        unique_together = (("tool", "cleared_user"),)
        verbose_name = _("Clearance")
        verbose_name_plural = _("Clearances")

    def __str__(self):
        return f"{self.cleared_by_user} cleared {self.cleared_user} ({self.tool})"


class ToolPhoto(TimeStampedModel):
    tool = models.ForeignKey(UserTool, on_delete=models.CASCADE, related_name="photos")
    uploading_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="uploaded_photos"
    )
    file = models.FileField()
    title = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ("-created",)
        get_latest_by = "created"
