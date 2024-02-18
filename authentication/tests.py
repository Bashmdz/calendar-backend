from django.test import TestCase
from .models import CustomUsers


class CustomUsersModelTestCase(TestCase):
    print("Running CustomUsersModelTestCase")

    def setUp(self):
        self.user = CustomUsers.objects.create_user(
            email="test@example.com", password="test123"
        )

    def test_create_user(self):
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(str(self.user), self.user.email)

    def test_unique_email(self):
        with self.assertRaises(Exception):
            CustomUsers.objects.create_user(
                email="test@example.com", password="test456"
            )

    def test_authentication(self):
        self.assertTrue(CustomUsers.objects.filter(email="test@example.com").exists())

    def test_authorization(self):
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()
        self.assertTrue(self.user.is_staff)
        self.assertTrue(self.user.is_superuser)
