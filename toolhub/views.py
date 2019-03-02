from django_jinja import views as jinja_views
from django.views.generic import DetailView

from tools.models import UserTool


class HomeView(DetailView):
    template_name = "home.jinja"
    context_object_name = "user"

    def get_object(self, qs=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        if ctx["user"].is_authenticated:
            ctx["borrowed_tools"] = UserTool.objects.borrowing_by_user(ctx["user"])
        return ctx


class ExceptionContextMixin:
    def get(self, *args, **kwargs):
        self.exception = kwargs.pop("exception", None)
        return super().get(*args, **kwargs)

    def get_context_data(self):
        context = super().get_context_data()
        context.update({"exception": self.exception})
        return context


class BadRequest(ExceptionContextMixin, jinja_views.BadRequest):
    pass


class PermissionDenied(ExceptionContextMixin, jinja_views.PermissionDenied):
    pass


class PageNotFound(ExceptionContextMixin, jinja_views.PageNotFound):
    pass


class ServerError(ExceptionContextMixin, jinja_views.ServerError):
    pass
