from django.urls import path

from borrowing.views import BorrowView, ReturnView

app_name = "borrowing"  # url namespace

urlpatterns = [
    path("<int:pk>/borrow/", BorrowView.as_view(), name="borrow"),
    path("<int:pk>/return/", ReturnView.as_view(), name="return"),
]
