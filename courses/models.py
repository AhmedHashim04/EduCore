from django.db import models
from academics.models import Department, Semester
from users.models import User

class Course(models.Model):
    code = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    credits = models.PositiveSmallIntegerField()
    description = models.TextField()
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True)
    is_core = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.code} - {self.title}"

class CourseOffering(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    instructor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                 limit_choices_to={'user_type': 2})
    section = models.CharField(max_length=10)
    capacity = models.PositiveSmallIntegerField()
    enrolled_students = models.PositiveSmallIntegerField(default=0)
    schedule = models.CharField(max_length=100, help_text="e.g., Mon/Wed 10:00-11:30")
    classroom = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('course', 'semester', 'section')
    
    def __str__(self):
        return f"{self.course.code} - {self.section} ({self.semester})"