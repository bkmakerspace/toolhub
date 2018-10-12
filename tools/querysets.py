from django.db.models import Q, QuerySet


class UserToolQuerySet(QuerySet):
    def for_user(self, user):
        return self.filter(user=user)

    def visible_to_user(self, user, own_tools=True):
        """Filter to the UserTools a user is allowed to view"""
        from tools.models import ToolClearance, ToolVisibility

        # user is on clearance list for tools marked as public or cleared
        cleared_tools = Q(
            permissions__cleared_user=user,
            clearance=ToolClearance.cleared.value,
            visibility__in=[
                ToolVisibility.public.value,
                ToolVisibility.cleared.value,
            ],
        )

        # all tools that have their visibility set to open
        open_tools = Q(visibility=ToolVisibility.public.value)

        # Show the user's own tools
        if not own_tools:
            own_tools = Q(user=user) | Q(
                visibility=ToolVisibility.private.value, user=user
            )
        else:
            own_tools = Q()

        return self.filter(cleared_tools | open_tools | own_tools)
