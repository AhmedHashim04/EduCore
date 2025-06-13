import factory
from django.contrib.auth import get_user_model
from academics.models import Department, Program, Semester
from courses.models import Course, CourseOffering
from assessment.models import Assignment, Submission, Exam, Grade
from student_services.models import Enrollment, StudentProfile, Attendance

User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    
    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.Sequence(lambda n: f'user{n}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'testpass123')
    user_type = 3  # Student by default

class DepartmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Department
    
    name = factory.Sequence(lambda n: f'Department {n}')
    code = factory.Sequence(lambda n: f'D{n:02d}')
    established_date = '2000-01-01'

class ProgramFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Program
    
    name = factory.Sequence(lambda n: f'Program {n}')
    code = factory.Sequence(lambda n: f'P{n:02d}')
    department = factory.SubFactory(DepartmentFactory)
    degree = 'BSc'
    duration = 4
    total_credits = 120

# Add more factories for other models...