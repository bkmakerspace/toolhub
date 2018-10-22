from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views.generic import TemplateView
import toolhub.views as toolhub_views


urlpatterns = [
    path("", TemplateView.as_view(template_name="home.jinja"), name="home"),
    path("", include("toolhub_auth.urls"), name="auth"),
    path("admin/", admin.site.urls),
    path("tools/", include("tools.urls"), name="tools"),
    path("markdownx/", include("markdownx.urls")),
]

handler400 = toolhub_views.BadRequest.as_view()
handler403 = toolhub_views.PermissionDenied.as_view()
handler404 = toolhub_views.PageNotFound.as_view()
handler500 = toolhub_views.ServerError.as_view()

if settings.DEBUG:
    import debug_toolbar

    # debug error templates
    urlpatterns += [
        path("400/", handler400, kwargs={"exception": Exception("Bad Request!")}),
        path("403/", handler403, kwargs={"exception": Exception("Permission Denied")}),
        path("404/", handler404, kwargs={"exception": Exception("Page not Found")}),
        path("500/", handler500),
    ]
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
