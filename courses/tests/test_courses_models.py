from django.test import TestCase
from academics.models import Department, Semester
from users.models import User
from courses.models import Course, CourseOffering

class CourseModelsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.department = Department.objects.create(
            name='Test Department',
            code='TD',
            established_date='2000-01-01'
        )
        
        cls.professor = User.objects.create_user(
            username='courseprof',
            email='prof@example.com',
            password='testpass123',
            user_type=2
        )
        
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
            capacity=30
        )

    def test_course_str(self):
        self.assertEqual(str(self.course), 'CS101 - Introduction to Testing')

    def test_offering_str(self):
        self.assertEqual(str(self.offering), 'CS101 - A (Fall 2023)')

    def test_offering_enrollment_count(self):
        self.assertEqual(self.offering.enrolled_students, 0)