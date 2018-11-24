from django.urls import path

from tools.views import (
    ClearUserView,
    OwnerUserToolFilterView,
    UserToolClearedView,
    UserToolCreateView,
    UserToolDeleteView,
    UserToolDetailView,
    UserToolHistoryView,
    UserToolFilterView,
    UserToolUpdateView,
    TaxDetailView,
    TaxTreeView,
)

app_name = "tools"  # url namespace

urlpatterns = [
    path("", UserToolFilterView.as_view(), name="home"),
    path("owned/", OwnerUserToolFilterView.as_view(), name="owned"),
    path("<int:pk>/", UserToolDetailView.as_view(), name="detail"),
    path("<int:pk>/history", UserToolHistoryView.as_view(), name="history"),
    path("<int:pk>/edit", UserToolUpdateView.as_view(), name="edit"),
    path("<int:pk>/clear", ClearUserView.as_view(), name="clear"),
    path("<int:pk>/cleared", UserToolClearedView.as_view(), name="cleared"),
    path("<int:pk>/delete", UserToolDeleteView.as_view(), name="delete"),
    path("create/", UserToolCreateView.as_view(), name="create"),
    path("tags/", TaxTreeView.as_view(), name="tags"),
    path("<path:path>/", TaxDetailView.as_view(), name="taxonomy_detail"),
]
