from django.db import models
from users.models import User
from academics.models import Program
from courses.models import TermCourse

from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
class Enrollment(models.Model):
    GRADE_CHOICES = (
        ('A', 'A'), ('A-', 'A-'), ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'),
        ('C+', 'C+'), ('C', 'C'), ('C-', 'C-'), ('D+', 'D+'), ('D', 'D'),
        ('F', 'F'), ('W', 'Withdrawn'), ('I', 'Incomplete'),
    )
    student = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        limit_choices_to={'user_type': 3}
    )
    course = models.ForeignKey(TermCourse, on_delete=models.CASCADE,related_name='enrollments')
    enrollment_date = models.DateTimeField(auto_now_add=True)
    grade = models.CharField(
        max_length=2, 
        choices=GRADE_CHOICES, 
        null=True, 
        blank=True
    )
    is_active = models.BooleanField(default=True)
    withdrawn = models.BooleanField(default=False)
    withdrawn_date = models.DateTimeField(null=True, blank=True)
    
    # New fields
    grade_points = models.DecimalField(
        max_digits=4, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    
    class Meta:
        unique_together = ('student', 'course')
        ordering = ['-enrollment_date']
    
    # Auto-set withdrawn_date when withdrawn
    def save(self, *args, **kwargs):
        if self.withdrawn and not self.withdrawn_date:
            self.withdrawn_date = timezone.now()
            self.is_active = False
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.student} in {self.course}"

class StudentProfile(models.Model):
    student = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        limit_choices_to={'user_type': 3},
        related_name='profile'
    )
    program = models.ForeignKey(
        Program, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    enrollment_date = models.DateField(auto_now_add=True)
    expected_graduation = models.DateField()
    current_semester = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    advisor = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        limit_choices_to={'user_type': 2}, 
        related_name='advisees'
    )
    gpa = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=0.00,
        validators=[MinValueValidator(0.00), MaxValueValidator(4.00)]
    )
    completed_credits = models.PositiveSmallIntegerField(default=0)
    
    # New fields
    academic_status = models.CharField(
        max_length=20,
        choices=(
            ('good', 'Good Standing'),
            ('probation', 'Academic Probation'),
            ('suspended', 'Suspended'),
        ),
        default='good'
    )
    transcript_key = models.CharField(max_length=50, blank=True, null=True)
    
    # Validation
    def clean(self):
        if self.expected_graduation < self.enrollment_date:
            raise ValidationError("Graduation date cannot be before enrollment date")
    
    def __str__(self):
        return f"{self.student}'s academic profile"


class Attendance(models.Model):
    course = models.ForeignKey(TermCourse, on_delete=models.CASCADE, related_name='attendances')
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
        unique_together = ('course', 'student', 'date')
    
    def __str__(self):
        return f"{self.student} - {self.date} - {self.get_status_display()}"