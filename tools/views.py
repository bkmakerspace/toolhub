from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.transaction import atomic
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, DetailView, DeleteView, ListView, UpdateView
from django_filters.views import FilterView

from tools.filters import UserToolFilterSet
from tools.forms import ClearancePermissionForm, UserToolCreateForm, UserToolUpdateForm
from tools.mixins import SingleToolObjectMixin, FilteredByToolObjectMixin
from tools.models import ClearancePermission, ToolHistory, UserTool
from utils.mixins import RestrictToUserMixin, VisibleToUserMixin


class UserToolBaseFilterView(FilterView):
    model = UserTool
    template_name = "tools/usertool_filter.jinja"
    context_object_name = "tools"
    filterset_class = UserToolFilterSet
    strict = False
    paginate_by = settings.DEFAULT_PAGINATE_BY

    def get_queryset(self):
        return super().get_queryset().select_related("user").prefetch_related("taxonomies")


class UserToolFilterView(VisibleToUserMixin, UserToolBaseFilterView):
    pass


class UserToolCreateView(LoginRequiredMixin, CreateView):
    """
    Allows user to create a new user tool
    """

    model = UserTool
    form_class = UserToolCreateForm
    template_name = "tools/usertool_create.jinja"
    # form_valid_message = _("Succefully added tool to your library.")

    def get_success_url(self):
        return self.object.get_absolute_url()

    @atomic
    def form_valid(self, form):
        user = self.request.user
        self.object = form.save(commit=False)
        self.object.user = user
        response = super(UserToolCreateView, self).form_valid(form)
        self.object.create(user=user, skip_save=True)
        return response


class UserToolUpdateView(RestrictToUserMixin, UpdateView):
    model = UserTool
    form_class = UserToolUpdateForm
    template_name = "tools/usertool_update.jinja"
    context_object_name = "tool"

    def get_success_url(self):
        return self.object.get_absolute_url()


class UserToolDetailView(VisibleToUserMixin, DetailView):
    model = UserTool
    template_name = "tools/usertool_detail.jinja"
    context_object_name = "tool"


class UserToolDeleteView(RestrictToUserMixin, DeleteView):
    model = UserTool
    template_name = "tools/usertool_delete.jinja"
    context_object_name = "tool"
    success_url = reverse_lazy("tools:owned")


class UserToolHistoryView(LoginRequiredMixin, FilteredByToolObjectMixin, ListView):
    model = ToolHistory
    tool_model = UserTool
    template_name = "tools/toolhistory_list.jinja"
    context_object_name = "history_items"
    paginate_by = settings.DEFAULT_PAGINATE_BY


class OwnerUserToolFilterView(RestrictToUserMixin, UserToolBaseFilterView):
    template_name = "tools/owner_usertool_filter.jinja"


# TOOD: swap out restrict to user mixin to a new mixin that checks clearance.
class ClearUserView(SingleToolObjectMixin, CreateView):
    """Clear a user to use a particular tool"""

    model = ClearancePermission
    tool_model = UserTool
    template_name = "tools/clearancepermission_form.jinja"
    form_class = ClearancePermissionForm

    def check_grant_perms(self, tool):
        if not self.tool.user_can_grant_clearance(self.request.user):
            raise PermissionDenied(_("You aren't allowed to give people access to this tool."))

    def get_initial(self):
        # Pass tool into initial arguments for form so it can be used for validation.
        return {"tool": self.tool}

    def get(self, request, *args, **kwargs):
        self.tool = self.get_tool()
        self.check_grant_perms(self.tool)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.tool = self.get_tool()
        self.check_grant_perms(self.tool)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        # attach data to form model instance so we don't have to send it in request.
        form.instance.cleared_by_user = self.request.user
        form.instance.tool = self.tool
        return super().form_valid(form)

    def get_success_url(self):
        return self.tool.get_absolute_url()


class UserToolClearedView(LoginRequiredMixin, FilteredByToolObjectMixin, ListView):
    model = ClearancePermission
    tool_model = UserTool
    template_name = "tools/usertool_clearred_list.jinja"
    context_object_name = "cleared_items"
    paginate_by = settings.DEFAULT_PAGINATE_BY
