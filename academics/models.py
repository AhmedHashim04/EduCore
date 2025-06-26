from django.db import models
from users.models import User

class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(null=True, blank=True)
    head_of_department = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                        limit_choices_to={'user_type': 2})
    established_date = models.DateField()
    website = models.URLField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class Program(models.Model):
    DEGREE_CHOICES = (
        ('BSc', 'Bachelor of Science'),
        ('BA', 'Bachelor of Arts'),
        ('MSc', 'Master of Science'),
        ('MA', 'Master of Arts'),
        ('PhD', 'Doctor of Philosophy'),
        
    )
    
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    degree = models.CharField(max_length=10, choices=DEGREE_CHOICES)
    duration = models.PositiveSmallIntegerField(help_text="Duration in years")
    description = models.TextField()
    total_credits = models.PositiveSmallIntegerField()
    
    def __str__(self):
        return f"{self.get_degree_display()} in {self.name}"

class Semester(models.Model):
    SEMESTER_CHOICES = (
        ('Fall', 'Fall'),
        ('Spring', 'Spring'),
        ('Summer', 'Summer'),
    )
    year = models.PositiveSmallIntegerField()
    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    registration_start = models.DateField()
    registration_end = models.DateField()
    is_current = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('year', 'semester')
        ordering = ['-year', 'semester']
    
    def __str__(self):
        return f"{self.get_semester_display()} {self.year}"