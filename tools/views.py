from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView
from django_filters.views import FilterView


from tools.filters import UserToolFilterSet
from tools.forms import CreateUserToolForm
from tools.models import UserTool
from utils.views import ContextMixin


class UserToolFilter(LoginRequiredMixin, ContextMixin, FilterView):
    model = UserTool
    template_name = "tools/usertool_filter.jinja"
    context_object_name = "tools"
    filterset_class = UserToolFilterSet
    strict = False

    def get_queryset(self):
        return self.model.objects.visible_to_user(self.request.user)


class CreateUserTool(LoginRequiredMixin, CreateView):
    """
    Allows user to create a new user tool
    """

    model = UserTool
    form_class = CreateUserToolForm
    template_name = "tools/usertool_create.jinja"
    form_valid_message = _("Succefully added tool to your library.")

    # fields = ('title', 'description', 'clearance')

    def get_success_url(self):
        return reverse("tools:home")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        return super(CreateUserTool, self).form_valid(form)
