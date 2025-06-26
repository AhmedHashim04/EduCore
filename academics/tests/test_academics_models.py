from django.test import TestCase
from users.models import User
from academics.models import Department, Program, Semester

class AcademicModelsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.professor = User.objects.create_user(
            username='depthead',
            email='head@example.com',
            password='testpass123',
            user_type=2
        )
        
        cls.department = Department.objects.create(
            name='Computer Science',
            code='CS',
            established_date='2000-01-01',
            head_of_department=cls.professor
        )
        
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

    def test_department_str(self):
        self.assertEqual(str(self.department), 'Computer Science')

    def test_program_str(self):
        self.assertEqual(str(self.program), 'Bachelor of Science in Computer Science')

    def test_semester_str(self):
        self.assertEqual(str(self.semester), 'Fall 2023')