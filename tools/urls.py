from django.urls import path

from tools.views import (
    ClearUserView,
    PrintLabelView,
    UserToolClearedView,
    UserToolCreateView,
    UserToolDeleteView,
    UserToolDetailView,
    UserToolHistoryView,
    UserToolFilterView,
    UserToolUpdateView,
    TaxDetailView,
    TaxTreeView,
    DecommissionView,
    ReinstateView,
    BorrowView,
    ReturnView,
)

app_name = "tools"  # url namespace


urlpatterns = [
    path("", UserToolFilterView.as_view(), name="home"),
    path("<int:pk>/", UserToolDetailView.as_view(), name="detail"),
    path("<int:pk>/label", PrintLabelView.as_view(), name="label"),
    path("<int:pk>/history", UserToolHistoryView.as_view(), name="history"),
    path("<int:pk>/edit", UserToolUpdateView.as_view(), name="edit"),
    path("<int:pk>/clear", ClearUserView.as_view(), name="clear"),
    path("<int:pk>/cleared", UserToolClearedView.as_view(), name="cleared"),
    path("<int:pk>/delete", UserToolDeleteView.as_view(), name="delete"),
    path("<int:pk>/borrow/", BorrowView.as_view(), name="borrow"),
    path("<int:pk>/return/", ReturnView.as_view(), name="return"),
    path("<int:pk>/decommission/", DecommissionView.as_view(), name="decommission"),
    path("<int:pk>/reinstate/", ReinstateView.as_view(), name="reinstate"),
    path("create/", UserToolCreateView.as_view(), name="create"),
    path("tags/", TaxTreeView.as_view(), name="tags"),
    path("<path:path>/", TaxDetailView.as_view(), name="taxonomy_detail"),
]
