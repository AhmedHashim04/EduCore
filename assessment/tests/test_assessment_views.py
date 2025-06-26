from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from tests.utils import TestSetupMixin

class AssessmentAPITests(TestSetupMixin, APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.department = cls.professor.professorprofile.department
        
        cls.course = Course.objects.create(
            code='CS101',
            title='Test Course',
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
        
        cls.assignment = Assignment.objects.create(
            course_offering=cls.offering,
            title='Test Assignment',
            description='This is a test',
            due_date=timezone.now() + timezone.timedelta(days=7),
            total_points=100,
            submission_type='text'
        )

    def test_assignment_creation_by_professor(self):
        client = self.get_authenticated_client(self.professor)
        url = reverse('assignment-list')
        data = {
            'course_offering': self.offering.id,
            'title': 'New Assignment',
            'description': 'Another test',
            'due_date': (timezone.now() + timezone.timedelta(days=14)).isoformat(),
            'total_points': 50,
            'submission_type': 'file'
        }
        response = client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_submission_creation_by_student(self):
        client = self.get_authenticated_client(self.student)
        url = reverse('submission-list')
        data = {
            'assignment': self.assignment.id,
            'text_entry': 'My test submission'
        }
        response = client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['text_entry'], 'My test submission')

    def test_grade_update_by_professor(self):
        # Create submission first
        submission = Submission.objects.create(
            assignment=self.assignment,
            student=self.student,
            text_entry='Test submission'
        )
        
        client = self.get_authenticated_client(self.professor)
        url = reverse('submission-detail', args=[submission.id])
        data = {
            'grade': 95,
            'feedback': 'Excellent work!'
        }
        response = client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['grade'], 95)