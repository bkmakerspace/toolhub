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
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices

# from model_utils.models import StatusModel, StatusField
from mptt.models import MPTTModel, TreeManager, TreeForeignKey


# SoftDeletableManager
class ToolTaxonomyManager(TreeManager):
    def published(self):
        return self.get_queryset().filter(status=ToolClassification.PUBLISHED)


# , StatusModel
class ToolTaxonomy(MPTTModel):
    name = models.CharField(max_length=255, unique=True, blank=False)
    slug = AutoSlugField(populate_from="name", max_length=255)

    # MPTT fields
    parent = TreeForeignKey("self", null=True, blank=True, related_name="children")
    order = models.IntegerField(blank=False, default=0)

    # publishing status. Allows users to submit new taxonomies,
    # that are evaluated and approved
    class State(Catalog):
        _attrs = "value", "label"
        in_review = 0, _("in review")
        published = 1, _("published")
        rejected = 2, _("rejected")

    state = models.PositiveSmallIntegerField(
        _("State"), choices=State._zip("value", "label"), default=State.in_review.value
    )
    locked = models.BooleanField(
        _("Locked"),
        help_text=_("locked taxonomoies can't be moved or edited."),
        default=False,
    )

    objects = ToolTaxonomyManager()

    class MPTTMeta:
        order_insertion_by = ["order"]

    class Meta:
        verbose_name = _("Tool Taxonomy")
        verbose_name_plural = _("Tool Taxonomies")
        unique_together = ("slug", "parent")

    def __str__(self):
        return self.name


class GenericTool(models.Model):
    pass
    """A Generic tool is a scaffold or cookie cutter instance of any combination of"""


class UserTool(models.Model):
    owner
    description

    pass
    """Owned by a user"""
