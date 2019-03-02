from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.transaction import atomic
from django import forms
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, DetailView, DeleteView, ListView, UpdateView
from django_filters.views import FilterView

from tools.filters import UserToolFilterSet
from tools.forms import ClearancePermissionForm, UserToolCreateForm, UserToolUpdateForm
from tools.mixins import SingleToolObjectMixin, FilteredByToolObjectMixin
from tools.models import ClearancePermission, ToolHistory, ToolTaxonomy, UserTool
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
        self.object.create(user=user)
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
class ClearUserView(SingleToolObjectMixin, UpdateView):
    """Clear users to use a particular tool"""

    model = UserTool
    tool_model = UserTool
    template_name = "tools/clearancepermission_form.jinja"
    form_class = ClearancePermissionForm

    def check_grant_perms(self, tool):
        if not self.tool.user_can_grant_clearance(self.request.user):
            raise PermissionDenied(_("You aren't allowed to give people access to this tool."))

    def get(self, request, *args, **kwargs):
        self.check_grant_perms(self.tool)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.check_grant_perms(self.tool)
        return super().post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["cleared_by_user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "User clearance updated.")
        return super().form_valid(form)

    def get_success_url(self):
        return self.tool.get_absolute_url()


class UserToolClearedView(LoginRequiredMixin, FilteredByToolObjectMixin, ListView):
    model = ClearancePermission
    tool_model = UserTool
    template_name = "tools/usertool_clearred_list.jinja"
    context_object_name = "cleared_items"
    paginate_by = settings.DEFAULT_PAGINATE_BY


class TaxTreeView(LoginRequiredMixin, ListView):
    model = ToolTaxonomy
    context_object_name = "tags"
    template_name = "tools/tag_tree.jinja"
    queryset = ToolTaxonomy.objects.filter(parent__isnull=True)


class TaxDetailView(LoginRequiredMixin, UserToolBaseFilterView):
    template_name = "tools/usertool_tax_filter.jinja"

    def get_queryset(self):
        path = self.kwargs.get("path", None)
        # handle not found
        tax = ToolTaxonomy.objects.get(path=path)
        decendant_ids = list(tax.get_descendants().values_list("id", flat=True))
        tax_ids = [tax.id] + decendant_ids
        ancestors = tax.get_ancestors()
        breadcrumbs = [(reverse_lazy("tools:home"), "Tools")]
        breadcrumbs += [(a.get_absolute_url(), a.name) for a in ancestors]
        breadcrumbs += [(None, tax.name)]
        self.extra_context = {"tax_breadcrumbs": breadcrumbs, "tax": tax}
        return super().get_queryset().filter(taxonomies__in=tax_ids)


class PrintLabelView(VisibleToUserMixin, DetailView):
    """
    Presents a template that is printable and shows a QR code link to a tools
    detail page.

    Allows for some customization via query parameters
    """

    model = UserTool
    template_name = "tools/usertool_label_detail.jinja"
    context_object_name = "tool"

    class PrintLabelOptions(forms.Form):
        # maps to CSS @page size propery value:
        ORIENTATION_CHOICES = ("landscape", "Landscape"), ("portrait", "Portrait")

        orientation = forms.ChoiceField(choices=ORIENTATION_CHOICES, required=False)
        force_print = forms.BooleanField(required=False)

    def get_tool_detail_url(self):
        return self.object.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        detail_link = self.get_tool_detail_url()

        qr_options = {"error_correction": "H", "border": 0, "image_format": "svg"}

        # set some default options
        data = dict(orientation="landscape", force_print=True)
        data.update(self.request.GET.dict())
        form = self.PrintLabelOptions(data)
        if not form.is_valid():
            context.update({"errors": form.errors})

        context.update(
            {
                "errors": None,
                "force_print": form.cleaned_data.get("force_print"),
                "page_orientation": form.cleaned_data.get("orientation"),
                "link": detail_link,
                "full_link": self.request.build_absolute_uri(detail_link),
                "qr_options": qr_options,
            }
        )
        return context
