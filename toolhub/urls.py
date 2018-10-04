from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    from django_jinja import views as jinja_views

    handler400 = jinja_views.BadRequest.as_view()
    handler403 = jinja_views.PermissionDenied.as_view()
    handler404 = jinja_views.PageNotFound.as_view()
    handler500 = jinja_views.ServerError.as_view()

    # debug error templates
    urlpatterns += [
        path("400/", handler400, kwargs={"exception": Exception("Bad Request!")}),
        path("403/", handler403, kwargs={"exception": Exception("Permission Denied")}),
        path("404/", handler404, kwargs={"exception": Exception("Page not Found")}),
        path("500/", handler500),
    ]
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
