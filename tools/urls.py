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
    UploadToolPhotoView,
)

app_name = "tools"  # url namespace

urlpatterns = [
    path("", UserToolFilterView.as_view(), name="home"),
    path("image_upload/", UploadToolPhotoView.as_view(), name="upload_tool_photo"),
    path("image_upload/<int:pk>/", UploadToolPhotoView.as_view(), name="upload_tool_photo"),
    path("<int:pk>/", UserToolDetailView.as_view(), name="detail"),
    path("<int:pk>/label", PrintLabelView.as_view(), name="label"),
    path("<int:pk>/history", UserToolHistoryView.as_view(), name="history"),
    path("<int:pk>/edit", UserToolUpdateView.as_view(), name="edit"),
    path("<int:pk>/clear", ClearUserView.as_view(), name="clear"),
    path("<int:pk>/cleared", UserToolClearedView.as_view(), name="cleared"),
    path("<int:pk>/delete", UserToolDeleteView.as_view(), name="delete"),
    path("create/", UserToolCreateView.as_view(), name="create"),
    path("tags/", TaxTreeView.as_view(), name="tags"),
    # TaxDetailView must stay at end to act as catch-all
    path("<path:path>/", TaxDetailView.as_view(), name="taxonomy_detail"),
]
