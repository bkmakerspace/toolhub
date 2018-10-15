from django.urls import path

from tools.views import CreateUserTool, UserToolDetail, UserToolFilter, UserToolHistory

app_name = "tools"  # url namespace

urlpatterns = [
    path("", UserToolFilter.as_view(), name="home"),
    path("<int:pk>/", UserToolDetail.as_view(), name="detail"),
    path("<int:pk>/history", UserToolHistory.as_view(), name="history"),
    path("create/", CreateUserTool.as_view(), name="create"),
]
