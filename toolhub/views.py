from django_jinja import views as jinja_views


class ExceptionContextMixin:
    def get(self, *args, **kwargs):
        self.exception = kwargs.pop('exception', None)
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
