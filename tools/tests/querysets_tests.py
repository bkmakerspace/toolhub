from django.conf import settings
from django.test import TestCase
from model_mommy import mommy

from tools.models import ToolHistory, UserTool
from tools.querysets import UserToolQuerySet


class UserToolQuerySetTests(TestCase):
    def make_tool(self, **kwargs):
        return mommy.make(UserTool, **kwargs)

    def setUp(self):
        self.qs = UserToolQuerySet(model=UserTool)
        self.user = mommy.make(settings.AUTH_USER_MODEL, first_name="bob")
        self.user_tool1 = self.make_tool(title="User owned", user=self.user)
        self.user_tool2 = self.make_tool(
            title="User owned set private",
            visibility=UserTool.Visibility.private.value,
            user=self.user,
        )
        self.user_tool3 = self.make_tool(
            title="User owned set private",
            visibility=UserTool.Visibility.cleared.value,
            user=self.user,
        )
        self.others_tool1 = self.make_tool(
            title="Someone elses public tool", visibility=UserTool.Visibility.public.value
        )
        self.others_tool_cleared_for_user = self.make_tool(
            title="Someone elses cleared tool for user",
            visibility=UserTool.Visibility.cleared.value,
        )

    def test_for_user(self):
        # tool for a different user
        self.make_tool(title="tool2", user__first_name="tommy")

        qs = self.qs.order_by("id").for_user(self.user)
        self.assertSequenceEqual(qs.all(), [self.user_tool1, self.user_tool2, self.user_tool3])

    def test_visible_to_user(self):
        """
        Users are allowed to see all their tools irelevant of status,
        any public tools, and tools they are cleared to use that may be set to cleared only.
        If a tool is set to private and they have clearance, they should not be able to see it.
        """
        # Tools that the user shouldn't be able to see
        self.make_tool(
            title="Someone elses private tool", visibility=UserTool.Visibility.private.value
        )
        cleared_to_user = self.make_tool(
            title="Someone elses private cleared to user",
            visibility=UserTool.Visibility.private.value,
        )
        self.make_tool(
            title="Someone elses cleared tool", visibility=UserTool.Visibility.cleared.value
        )

        # Give user permissions
        mommy.make(
            "tools.ClearancePermission",
            tool=self.others_tool_cleared_for_user,
            cleared_by_user=self.others_tool_cleared_for_user.user,
            cleared_user=self.user,
        )
        # shouldn't show up on list, event though user is cleared
        mommy.make(
            "tools.ClearancePermission",
            tool=cleared_to_user,
            cleared_by_user=cleared_to_user.user,
            cleared_user=self.user,
        )
        # Give another user permission to own tool, should not effect results
        mommy.make(
            "tools.ClearancePermission",
            tool=self.user_tool1,
            cleared_user=self.others_tool1.user,
            cleared_by_user=self.user,
        )

        qs = self.qs.order_by("id").visible_to_user(self.user)
        self.assertSequenceEqual(
            list(qs.all()),
            [
                self.user_tool1,
                self.user_tool2,
                self.user_tool3,
                self.others_tool1,
                self.others_tool_cleared_for_user,
            ],
        )

    def test_visible_to_user_include_users_tools_false(self):
        """
        When include_users_tools kwarg is false we don't see the user's private
        or cleared only tools
        """
        # Tools that the user shouldn't be able to see
        self.make_tool(
            title="Someone elses private tool", visibility=UserTool.Visibility.private.value
        )
        cleared_to_user = self.make_tool(
            title="Someone elses private cleared to user",
            visibility=UserTool.Visibility.private.value,
        )
        self.make_tool(
            title="Someone elses cleared tool", visibility=UserTool.Visibility.cleared.value
        )

        # Give user permissions
        mommy.make(
            "tools.ClearancePermission",
            tool=self.others_tool_cleared_for_user,
            cleared_by_user=self.others_tool_cleared_for_user.user,
            cleared_user=self.user,
        )
        # shouldn't show up on list, event though user is cleared
        mommy.make(
            "tools.ClearancePermission",
            tool=cleared_to_user,
            cleared_by_user=cleared_to_user.user,
            cleared_user=self.user,
        )
        # Give another user permission to own tool, should not effect results
        mommy.make(
            "tools.ClearancePermission",
            tool=self.user_tool1,
            cleared_user=self.others_tool1.user,
            cleared_by_user=self.user,
        )

        qs = self.qs.order_by("id").visible_to_user(self.user, include_users_tools=False)
        self.assertSequenceEqual(
            list(qs.all()), [self.user_tool1, self.others_tool1, self.others_tool_cleared_for_user]
        )

    def xtest_borrowing_by_user(self):

        borrowed = self.make_tool(
            title="A previously borrowed tool", state=UserTool.States.in_use.value
        )

        returned = self.make_tool(
            title="A previously borrowed tool, returned", state=UserTool.States.available.value
        )

        # Borrowed by another user
        mommy.make(ToolHistory, tool=borrowed, action=UserTool.Transitions.borrow.value)
        mommy.make(ToolHistory, tool=returned, action=UserTool.Transitions.borrow.value)
        # Both returned
        mommy.make(ToolHistory, tool=borrowed, action=UserTool.Transitions.return_.value)
        mommy.make(ToolHistory, tool=returned, action=UserTool.Transitions.return_.value)
        # Both are borrowed by test user
        mommy.make(
            ToolHistory, tool=borrowed, user=self.user, action=UserTool.Transitions.borrow.value
        )
        mommy.make(
            ToolHistory, tool=returned, user=self.user, action=UserTool.Transitions.borrow.value
        )
        # One is returned
        mommy.make(
            ToolHistory, tool=returned, user=self.user, action=UserTool.Transitions.return_.value
        )

        result = UserTool.objects.borrowing_by_user(self.user)
        self.assertSequenceEqual(list(result.all()), [borrowed])
