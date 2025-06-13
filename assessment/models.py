from django.db import models
from courses.models import CourseOffering
from users.models import User

class Assignment(models.Model):
    course_offering = models.ForeignKey(CourseOffering, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    total_points = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    submission_type = models.CharField(max_length=50, choices=(
        ('file', 'File Upload'),
        ('text', 'Text Entry'),
        ('both', 'Both'),
    ), default='file')
    
    def __str__(self):
        return f"{self.title} - {self.course_offering}"

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 3})
    submitted_at = models.DateTimeField(auto_now_add=True)
    text_entry = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='submissions/', null=True, blank=True)
    grade = models.PositiveSmallIntegerField(null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)
    is_late = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('assignment', 'student')
    
    def __str__(self):
        return f"{self.student}'s submission for {self.assignment}"

class Exam(models.Model):
    EXAM_TYPE_CHOICES = (
        ('midterm', 'Midterm Exam'),
        ('final', 'Final Exam'),
        ('quiz', 'Quiz'),
        ('project', 'Project'),
    )
    
    course_offering = models.ForeignKey(CourseOffering, on_delete=models.CASCADE)
    exam_type = models.CharField(max_length=10, choices=EXAM_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    date = models.DateTimeField()
    total_points = models.PositiveSmallIntegerField()
    weight = models.PositiveSmallIntegerField(help_text="Weight in percentage")
    location = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return f"{self.get_exam_type_display()} - {self.course_offering}"

class Grade(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 3})
    score = models.PositiveSmallIntegerField()
    comments = models.TextField(null=True, blank=True)
    published = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('exam', 'student')
    
    def __str__(self):
        return f"{self.student}'s grade for {self.exam}"