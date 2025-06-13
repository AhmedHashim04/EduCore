from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from tests.utils import TestSetupMixin

class AcademicAPITests(TestSetupMixin, APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.department = cls.professor.professorprofile.department
        
        cls.program = Program.objects.create(
            name='Computer Science',
            code='CS01',
            department=cls.department,
            degree='BSc',
            duration=4,
            total_credits=120
        )
        
        cls.semester = Semester.objects.create(
            year=2023,
            semester='Fall',
            start_date='2023-09-01',
            end_date='2023-12-15'
        )

    def test_department_list(self):
        client = self.get_authenticated_client(self.student)
        url = reverse('department-list')
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_program_filtering(self):
        client = self.get_authenticated_client(self.student)
        url = f"{reverse('program-list')}?department={self.department.id}"
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], 'Computer Science')

    def test_semester_creation_admin_only(self):
        client = self.get_authenticated_client(self.student)
        url = reverse('semester-list')
        data = {
            'year': 2024,
            'semester': 'Spring',
            'start_date': '2024-01-15',
            'end_date': '2024-05-01'
        }
        response = client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Admin can create
        client = self.get_authenticated_client(self.admin)
        response = client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)