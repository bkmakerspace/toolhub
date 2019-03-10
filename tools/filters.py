from django.utils.translation import ugettext_lazy as _
from django_filters import FilterSet, filters

from toolhub_auth.models import User

from .forms import UserToolFilterViewForm
from .models import UserTool


class UserToolFilterSet(FilterSet):
    name = filters.CharFilter(field_name="title", lookup_expr="icontains", label=_("Tool name"))
    borrower = filters.ModelChoiceFilter(
        method="filter_by_borrower", queryset=User.objects.none(), label=_("Borrower")
    )

    class Meta:
        model = UserTool
        fields = ("name", "taxonomies", "state", "user")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters["user"].label = "Owner"
        self.filters["borrower"].queryset = User.objects.filter(is_active=True)

    def get_form_class(self):
        default_class = super().get_form_class()
        fields = default_class.base_fields
        return type(str("%sForm" % self.__class__.__name__), (UserToolFilterViewForm,), fields)

    def filter_by_borrower(self, qs, name, value):
        return qs.borrowing_by_user(value)
