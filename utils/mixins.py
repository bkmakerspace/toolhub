from django.contrib.auth.mixins import LoginRequiredMixin


class RestrictToUserMixin(LoginRequiredMixin):
    """
    View mixin for SingleObjectMixin views that restricts the
    queryset to only objects related to the request user.

    specify the model foreign key field with property: restrict_user_field
    """

    restrict_user_field = "user"

    def get_queryset(self):
        return super().get_queryset().filter(**{self.restrict_user_field: self.request.user})


class VisibleToUserMixin(LoginRequiredMixin):
    def get_queryset(self):
        return super().get_queryset().visible_to_user(self.request.user)
