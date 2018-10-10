from django.urls import path

from tools.views import CreateUserTool, UserToolFilter

app_name = "tools"  # url namespace

urlpatterns = [
    path("", UserToolFilter.as_view(), name="home"),
    path("create/", CreateUserTool.as_view(), name="create"),
]
