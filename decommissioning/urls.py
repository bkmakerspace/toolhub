from django.urls import path

from decommissioning.views import DecommissionView, ReinstateView

app_name = "decommissioning"

urlpatterns = [
    path("<int:pk>/decommission/", DecommissionView.as_view(), name="decommission"),
    path("<int:pk>/reinstate/", ReinstateView.as_view(), name="reinstate"),
]
