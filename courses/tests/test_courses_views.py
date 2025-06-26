from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from tests.utils import TestSetupMixin

class CourseAPITests(TestSetupMixin, APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.department = cls.professor.professorprofile.department
        
        cls.course = Course.objects.create(
            code='CS101',
            title='Introduction to Testing',
            department=cls.department,
            credits=3
        )
        
        cls.semester = Semester.objects.create(
            year=2023,
            semester='Fall',
            start_date='2023-09-01',
            end_date='2023-12-15'
        )
        
        cls.offering = CourseOffering.objects.create(
            course=cls.course,
            semester=cls.semester,
            instructor=cls.professor,
            section='A',
            capacity=30,
            schedule='Mon/Wed 10:00-11:30'
        )

    def test_course_search(self):
        client = self.get_authenticated_client(self.student)
        url = f"{reverse('course-list')}?search=Testing"
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Introduction to Testing')

    def test_offering_creation_professor_permissions(self):
        client = self.get_authenticated_client(self.professor)
        url = reverse('offering-list')
        data = {
            'course': self.course.id,
            'semester': self.semester.id,
            'section': 'B',
            'capacity': 25,
            'schedule': 'Tue/Thu 14:00-15:30'
        }
        response = client.post(url, data)
        
        # Professors shouldn't be able to create offerings
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_offering_filter_by_semester(self):
        client = self.get_authenticated_client(self.student)
        url = f"{reverse('offering-list')}?semester_id={self.semester.id}"
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['section'], 'A')