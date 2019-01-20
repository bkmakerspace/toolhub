from django.test import TestCase
from model_mommy import mommy


class TestUser(TestCase):
    def test_profile_created_on_inital_save(self):
        user = mommy.make('toolhub_auth.User', first_name='Test', last_name='User')

        self.assertEqual(str(user.profile), 'Test User profile')
