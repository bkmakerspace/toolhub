from django.urls import path

from tools.views import CreateUserTool, UserToolList

app_name = 'tools'  #url namespace

urlpatterns = [
    path('', UserToolList.as_view(), name='home'),
    path('create/', CreateUserTool.as_view(), name='create'),
]

