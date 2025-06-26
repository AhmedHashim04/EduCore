from django.test import TestCase
from users.models import User
from academics.models import Department, Program
from courses.models import Course, CourseOffering, Semester
from student_services.models import Enrollment, StudentProfile, Attendance

class StudentServicesModelsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        department = Department.objects.create(
            name='Test Department',
            code='TD',
            established_date='2000-01-01'
        )
        
        cls.program = Program.objects.create(
            name='Test Program',
            code='TP01',
            department=department,
            degree='BSc',
            duration=4,
            total_credits=120
        )
        
        cls.professor = User.objects.create_user(
            username='testprof',
            email='prof@example.com',
            password='testpass123',
            user_type=2
        )
        
        cls.student = User.objects.create_user(
            username='teststudent',
            email='student@example.com',
            password='testpass123',
            user_type=3
        )
        
        cls.student_profile = StudentProfile.objects.create(
            student=cls.student,
            program=cls.program,
            enrollment_date='2023-09-01',
            expected_graduation='2027-06-01',
            current_semester=1,
            advisor=cls.professor
        )
        
        course = Course.objects.create(
            code='CS101',
            title='Test Course',
            department=department,
            credits=3
        )
        
        semester = Semester.objects.create(
            year=2023,
            semester='Fall',
            start_date='2023-09-01',
            end_date='2023-12-15'
        )
        
        cls.offering = CourseOffering.objects.create(
            course=course,
            semester=semester,
            instructor=cls.professor,
            section='A',
            capacity=30
        )
        
        cls.enrollment = Enrollment.objects.create(
            student=cls.student,
            course_offering=cls.offering
        )
        
        cls.attendance = Attendance.objects.create(
            student=cls.student,
            course_offering=cls.offering,
            date='2023-09-05',
            status='P'
        )

    def test_enrollment_str(self):
        self.assertEqual(str(self.enrollment), 'teststudent in CS101 - A (Fall 2023)')

    def test_student_profile_str(self):
        self.assertEqual(str(self.student_profile), "teststudent's academic profile")

    def test_attendance_str(self):
        self.assertEqual(str(self.attendance), 'teststudent - 2023-09-05 - Present')