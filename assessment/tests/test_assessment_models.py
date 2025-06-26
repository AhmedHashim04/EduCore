from django.test import TestCase
from django.utils import timezone
from courses.models import Course, CourseOffering, Semester
from users.models import User
from assessment.models import Assignment, Submission, Exam, Grade

class AssessmentModelsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        department = Department.objects.create(
            name='Test Department',
            code='TD',
            established_date='2000-01-01'
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
        
        cls.assignment = Assignment.objects.create(
            course_offering=cls.offering,
            title='Test Assignment',
            description='This is a test',
            due_date=timezone.now() + timezone.timedelta(days=7),
            total_points=100
        )
        
        cls.submission = Submission.objects.create(
            assignment=cls.assignment,
            student=cls.student,
            text_entry='My test submission'
        )
        
        cls.exam = Exam.objects.create(
            course_offering=cls.offering,
            exam_type='midterm',
            title='Midterm Exam',
            date=timezone.now() + timezone.timedelta(days=14),
            total_points=100,
            weight=30
        )
        
        cls.grade = Grade.objects.create(
            exam=cls.exam,
            student=cls.student,
            score=85
        )

    def test_assignment_str(self):
        self.assertEqual(str(self.assignment), 'Test Assignment - CS101 - A (Fall 2023)')

    def test_submission_str(self):
        self.assertEqual(str(self.submission), "teststudent's submission for Test Assignment - CS101 - A (Fall 2023)")

    def test_exam_str(self):
        self.assertEqual(str(self.exam), 'Midterm Exam - CS101 - A (Fall 2023)')

    def test_grade_str(self):
        self.assertEqual(str(self.grade), "teststudent's grade for Midterm Exam - CS101 - A (Fall 2023)")