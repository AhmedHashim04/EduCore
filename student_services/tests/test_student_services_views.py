from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from tests.utils import TestSetupMixin

class StudentServicesAPITests(TestSetupMixin, APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.department = cls.professor.professorprofile.department
        
        cls.program = Program.objects.create(
            name='Test Program',
            code='TP01',
            department=cls.department,
            degree='BSc',
            duration=4,
            total_credits=120
        )
        
        cls.student_profile = StudentProfile.objects.create(
            student=cls.student,
            program=cls.program,
            enrollment_date='2023-09-01',
            expected_graduation='2027-06-01',
            current_semester=1,
            advisor=cls.professor
        )
        
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
        
        cls.enrollment = Enrollment.objects.create(
            student=cls.student,
            course_offering=cls.offering
        )

    def test_student_profile_retrieve(self):
        client = self.get_authenticated_client(self.student)
        url = reverse('profile-detail', args=[self.student_profile.id])
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['program']['name'], 'Test Program')

    def test_enrollment_list_for_student(self):
        client = self.get_authenticated_client(self.student)
        url = f"{reverse('enrollment-list')}?student={self.student.id}"
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['course_offering']['course']['code'], 'CS101')

    def test_attendance_creation_by_professor(self):
        client = self.get_authenticated_client(self.professor)
        url = reverse('attendance-list')
        data = {
            'student': self.student.id,
            'course_offering': self.offering.id,
            'date': '2023-09-12',
            'status': 'P'
        }
        response = client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'P')