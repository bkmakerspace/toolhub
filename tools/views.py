from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.transaction import atomic
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.views.generic.detail import SingleObjectMixin
from django_filters.views import FilterView

from tools.filters import UserToolFilterSet
from tools.forms import UserToolCreateForm, UserToolUpdateForm
from tools.models import ToolHistory, UserTool
from utils.mixins import RestrictToUserMixin


class UserToolFilterView(LoginRequiredMixin, FilterView):
    model = UserTool
    template_name = "tools/usertool_filter.jinja"
    context_object_name = "tools"
    filterset_class = UserToolFilterSet
    strict = False
    paginate_by = settings.DEFAULT_PAGINATE_BY

    def get_queryset(self):
        return self.model.objects.visible_to_user(self.request.user).select_related(
            "user"
        ).prefetch_related("taxonomies")


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


class UserToolDetailView(LoginRequiredMixin, DetailView):
    model = UserTool
    template_name = "tools/usertool_detail.jinja"
    context_object_name = "tool"

    def get_queryset(self):
        return self.model.objects.visible_to_user(self.request.user)


class UserToolHistoryView(LoginRequiredMixin, ListView, SingleObjectMixin):
    model = ToolHistory
    template_name = "tools/toolhistory_list.jinja"
    context_object_name = 'history_items'
    pk_url_kwarg = 'pk'
    paginate_by = settings.DEFAULT_PAGINATE_BY

    def get_queryset(self):
        # TODO make sure this doesn't allow people w/o permissions to view
        tool = self.get_object(UserTool.objects.visible_to_user(self.request.user))
        self.object = tool
        self.extra_context = {"tool": self.object}
        queryset = super().get_queryset().filter(tool=tool)
        return queryset
