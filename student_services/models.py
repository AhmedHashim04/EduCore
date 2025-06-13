from django.db import models
from users.models import User
from academics.models import Program
from courses.models import CourseOffering

class Enrollment(models.Model):
    GRADE_CHOICES = (
        ('A', 'A'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B', 'B'),
        ('B-', 'B-'),
        ('C+', 'C+'),
        ('C', 'C'),
        ('C-', 'C-'),
        ('D+', 'D+'),
        ('D', 'D'),
        ('F', 'F'),
        ('W', 'Withdrawn'),
        ('I', 'Incomplete'),
    )
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 3})
    course_offering = models.ForeignKey(CourseOffering, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    withdrawn = models.BooleanField(default=False)
    withdrawn_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('student', 'course_offering')
    
    def __str__(self):
        return f"{self.student} in {self.course_offering}"

class StudentProfile(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 3})
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True, blank=True)
    enrollment_date = models.DateField()
    expected_graduation = models.DateField()
    current_semester = models.PositiveSmallIntegerField(default=1)
    advisor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                              limit_choices_to={'user_type': 2})
    gpa = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    completed_credits = models.PositiveSmallIntegerField(default=0)
    
    def __str__(self):
        return f"{self.student}'s academic profile"

class Attendance(models.Model):
    course_offering = models.ForeignKey(CourseOffering, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 3})
    date = models.DateField()
    status = models.CharField(max_length=1, choices=(
        ('P', 'Present'),
        ('A', 'Absent'),
        ('L', 'Late'),
        ('E', 'Excused'),
    ), default='P')
    notes = models.TextField(null=True, blank=True)
    
    class Meta:
        unique_together = ('course_offering', 'student', 'date')
    
    def __str__(self):
        return f"{self.student} - {self.date} - {self.get_status_display()}"