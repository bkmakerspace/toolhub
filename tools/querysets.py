from django.contrib.auth import get_user_model
from django.db.models import Q, QuerySet, Subquery, OuterRef

User = get_user_model()


class UserToolQuerySet(QuerySet):
    def for_user(self, user: User) -> QuerySet:
        return self.filter(user=user)

    def _cleared_tools_query(self, user: User) -> Q:
        """Query object of all tools a user as clearance to that are visible

        Args:
            user (User): The user who we are checking for clearance

        Returns:
            Q
        """
        return Q(
            permissions__cleared_user=user,
            visibility__in=[
                self.model.Visibility.public.value,
                self.model.Visibility.cleared.value,
            ],
        )

    def _open_tools_query(self) -> Q:
        """Query object of all tools that have their visibility set to public

        Returns:
            Q
        """
        return Q(visibility=self.model.Visibility.public.value)

    def _enabled_tools_query(self) -> Q:
        """Query object of all tools that have not been decommissioned

        Returns:
            Q
        """
        return ~Q(state=self.model.States.disabled.value)

    def visible_to_user(self, user: User, include_users_tools=True) -> QuerySet:
        """Filter to the UserTools a user is allowed to view

        Args:
            user (User): The user who we are checking tool visibility for
            include_users_tools (bool, optional): Also include the tools a user owns

        Returns:
            QuerySet
        """
        cleared_tools = self._cleared_tools_query(user)
        open_tools = self._open_tools_query()

        # Show the user's own tools
        if include_users_tools:
            own_tools = Q(
                visibility__in=[
                    self.model.Visibility.private.value,
                    self.model.Visibility.cleared.value,
                ],
                user=user,
            )
        else:
            own_tools = Q()

        return self.filter(cleared_tools | open_tools | own_tools).distinct()

    def borrowable_to_user(self, user: User) -> QuerySet:
        """Filter tools that a user is able to borrow

        Args:
            user (User): The user who we are checking the borrowability status for

        Returns:
            QuerySet
        """
        all_users_tools = Q(user=user)
        return self.filter(
            self._enabled_tools_query() & (self._cleared_tools_query(user) | self._open_tools_query() | all_users_tools)
        )

    def borrowing_by_user(self, user: User, exclude_own=False) -> QuerySet:
        """Return a QS of all tools a user is currently borrowing

        Args:
            user (User): The use who we are filtering tools to what they are currently borrowing
            exclude_own (bool, optional): Description

        Returns:
            QuerySet
        """
        from tools.models import ToolHistory

        history_qs = ToolHistory.objects.filter(tool=OuterRef("pk"), user=user).order_by(
            "-created"
        )
        qs = self
        if exclude_own:
            qs = qs.exclude(user=user)
        return qs.annotate(
            last_history_action=Subquery(history_qs.values("action")[:1]),
            last_history_date=Subquery(history_qs.values("created")[:1]),
        ).filter(
            state=self.model.States.in_use.value,
            last_history_action=self.model.Transitions.borrow.value,
        )


class ToolHistoryQuerySet(QuerySet):
    def latest_borrow(self):
        from tools.models import UserTool

        return self.filter(action=UserTool.Transitions.borrow.value).latest()
