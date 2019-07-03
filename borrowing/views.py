"""
There are different ways to accept a leanding request,
you can get an email and click a link with a one time use token to accept or deny a request
Or view the tools page to view pending requests. There can be stacked pending requests
There needs to be new models for handling requests.

TODO: maybe change verbiage to borrowing?
focus on web based borrowing first. Provide an state interface via the state machine or other
means that allows multiple interaction points to perform the borrowing operations

Phases:
Requested: if a user doesn't have permission to use a tool and it's visible to them,
they are given option to request a lend.

Lended:
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View

from tools.mixins import SingleToolObjectMixin
from tools.models import UserTool
from utils.transitions.mixins import ActionViewMixin


class BorrowView(ActionViewMixin, LoginRequiredMixin, SingleToolObjectMixin, View):
    """
    Process a request to borrow a tool
    """

    tool_model = UserTool
    transition_name = "borrow"
    object_class_attribute = "tool"
    transition_success_message = _("Borrowed tool")
    transition_failed_message = _("Can't borrow tool")


class ReturnView(ActionViewMixin, LoginRequiredMixin, SingleToolObjectMixin, View):
    """
    Process a request to return a tool
    """

    tool_model = UserTool
    transition_name = "return_"
    object_class_attribute = "tool"
    transition_success_message = _("Returned tool")
    transition_failed_message = _("Can't return tool")
