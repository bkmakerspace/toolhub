from django.conf import settings
from django.test import TestCase
from model_mommy import mommy

from tools.models import UserTool
from tools.querysets import UserToolQuerySet


class UserToolQuerySetTests(TestCase):
    def setUp(self):
        self.qs = UserToolQuerySet(model=UserTool)

    def test_for_user(self):
        user = mommy.make(settings.AUTH_USER_MODEL, first_name="bob")

        # tools
        tool1 = mommy.make(UserTool, title="tool1", user=user)
        tool2 = mommy.make(UserTool, title="tool2", user__first_name="tommy")

        qs = self.qs.for_user(user)
        self.assertSequenceEqual(qs.all(), [tool1])

    def test_visible_to_user(self):
        pass
