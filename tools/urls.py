from django.urls import path

from tools.views import CreateUserTool, UserToolDetail, UserToolFilter

app_name = "tools"  # url namespace

urlpatterns = [
    path("", UserToolFilter.as_view(), name="home"),
    path("<int:pk>/", UserToolDetail.as_view(), name="detail"),
    path("create/", CreateUserTool.as_view(), name="create"),
]
