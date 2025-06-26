from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from tests.utils import TestSetupMixin

class UserAPITests(TestSetupMixin, APITestCase):
    def test_user_registration(self):
        url = reverse('register')
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'testpass123',
            'user_type': 3,
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'newuser')

    def test_token_obtain(self):
        url = reverse('token_obtain_pair')
        data = {
            'username': 'student1',
            'password': 'testpass123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_profile_retrieve(self):
        client = self.get_authenticated_client(self.student)
        url = reverse('profile')
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'student1')

    def test_user_list_permissions(self):
        # Unauthenticated
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Student trying to access
        client = self.get_authenticated_client(self.student)
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Admin access
        client = self.get_authenticated_client(self.admin)
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)