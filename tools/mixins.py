from django.http import Http404
from django.utils.translation import ugettext_lazy as _


class SingleToolObjectMixin:
    tool_pk_url_kwarg = "pk"
    tool_context_object_name = "tool"
    tool_model = None
    _tool = None

    def get_tool(self):
        if self._tool:
            return self._tool

        assert self.request.user

        pk = self.kwargs.get(self.tool_pk_url_kwarg, None)
        queryset = self.tool_model.objects.visible_to_user(self.request.user)

        if pk is not None:
            queryset = queryset.filter(pk=pk)

        # If none of those are defined, it's an error.
        if pk is None:
            raise AttributeError(
                "%s must be called with a tool object "
                "pk in the URLconf." % self.__class__.__name__
            )

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
            self._tool = obj
        except self.tool_model.DoesNotExist:
            raise Http404(
                _("No %(verbose_name)s found matching the query")
                % {"verbose_name": queryset.model._meta.verbose_name}
            )
        return obj

    def get_context_data(self, **kwargs):
        tool = self.get_tool()
        if self.extra_context is None:
            self.extra_context = {}
        self.extra_context.update({self.tool_context_object_name: tool})
        return super().get_context_data(**kwargs)


class FilteredByToolObjectMixin(SingleToolObjectMixin):
    tool_rel_lookup = "tool"

    def get_queryset(self):
        """Restrict queryset to found tool"""
        tool = self.get_tool()
        return super().get_queryset().filter(**{self.tool_rel_lookup: tool})
