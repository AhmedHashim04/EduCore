from django.test import TestCase
from django.core.exceptions import ValidationError
from users.models import User

class UserModelTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            user_type=3
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.user_type, 3)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            username='superuser',
            email='super@example.com',
            password='testpass123'
        )
        self.assertEqual(admin.user_type, 1)
        self.assertTrue(admin.is_active)
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_user_str(self):
        user = User.objects.create_user(
            username='strtest',
            email='str@example.com',
            password='testpass123',
            user_type=2
        )
        self.assertEqual(str(user), 'strtest (Professor)')