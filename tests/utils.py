from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class TestSetupMixin:
    @classmethod
    def setUpTestData(cls):
        # Create test users
        cls.admin = User.objects.create_superuser(
            username='admin',
            email='admin@college.edu',
            password='testpass123',
            user_type=1
        )
        
        cls.professor = User.objects.create_user(
            username='professor1',
            email='professor1@college.edu',
            password='testpass123',
            user_type=2
        )
        
        cls.student = User.objects.create_user(
            username='student1',
            email='student1@college.edu',
            password='testpass123',
            user_type=3
        )
        
        cls.staff = User.objects.create_user(
            username='staff1',
            email='staff1@college.edu',
            password='testpass123',
            user_type=4
        )

    def get_authenticated_client(self, user):
        client = APIClient()
        refresh = RefreshToken.for_user(user)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        return client

    def assertResponseDetail(self, response, detail):
        self.assertEqual(response.data.get('detail'), detail)

    def assertValidationError(self, response, field):
        self.assertIn(field, response.data)