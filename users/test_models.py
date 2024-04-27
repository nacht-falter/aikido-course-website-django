from django.test import TestCase
from django.utils.text import slugify

from .models import User, UserProfile


class TestUserProfileModel(TestCase):
    """Tests for UserProfile model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="test-user",
            password="testpassword",
        )
        self.client.force_login(self.user)
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            grade=0,
        )

    def test_user_profile_slug(self):
        print("\ntest_user_profile_slug")
        self.assertEqual(self.user_profile.slug, slugify(self.user.username))
