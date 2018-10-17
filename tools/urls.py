from django.urls import path

from tools.views import (
    OwnerUserToolFilterView,
    UserToolCreateView,
    UserToolDetailView,
    UserToolHistoryView,
    UserToolFilterView,
    UserToolUpdateView,
)

app_name = "tools"  # url namespace

urlpatterns = [
    path("", UserToolFilterView.as_view(), name="home"),
    path("owned/", OwnerUserToolFilterView.as_view(), name="owned"),
    path("<int:pk>/", UserToolDetailView.as_view(), name="detail"),
    path("<int:pk>/history", UserToolHistoryView.as_view(), name="history"),
    path("<int:pk>/edit", UserToolUpdateView.as_view(), name="edit"),
    path("create/", UserToolCreateView.as_view(), name="create"),
]
