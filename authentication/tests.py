from django.test import TestCase
from .models import CustomUsers


class CustomUsersModelTestCase(TestCase):
    # Test case for CustomUsers model

    def setUp(self):
        # Set up the test case
        self.user = CustomUsers.objects.create_user(
            email="test@example.com", password="test123"
        )

    def test_create_user(self):
        # Test creating a user
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(str(self.user), self.user.email)

    def test_unique_email(self):
        # Test uniqueness of email
        with self.assertRaises(Exception):
            CustomUsers.objects.create_user(
                email="test@example.com", password="test456"
            )

    def test_authentication(self):
        # Test user authentication
        self.assertTrue(CustomUsers.objects.filter(email="test@example.com").exists())

    def test_authorization(self):
        # Test user authorization
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()
        self.assertTrue(self.user.is_staff)
        self.assertTrue(self.user.is_superuser)
