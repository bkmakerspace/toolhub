from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View

from tools.mixins import SingleToolObjectMixin
from tools.models import UserTool
from utils.transitions.mixins import ActionViewMixin


class DecommissionView(ActionViewMixin, LoginRequiredMixin, SingleToolObjectMixin, View):
    """
    Process a request to decommission a tool
    """

    tool_model = UserTool
    transition_name = "decommission"
    object_class_attribute = "tool"
    transition_success_message = _("Decommissioned tool")
    transition_failed_message = _("Can't decommission tool")


class ReinstateView(ActionViewMixin, LoginRequiredMixin, SingleToolObjectMixin, View):
    """
    Process a request to reinstate a tool
    """

    tool_model = UserTool
    transition_name = "reinstate"
    object_class_attribute = "tool"
    transition_success_message = _("Reinstated tool")
    transition_failed_message = _("Can't reinstate tool")
