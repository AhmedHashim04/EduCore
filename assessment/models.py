from django.db import models
from courses.models import TermCourse
from users.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

class Assignment(models.Model):
    course = models.ForeignKey(TermCourse, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    total_points = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    submission_type = models.CharField(
        max_length=50, 
        choices=(
            ('file', 'File Upload'),
            ('text', 'Text Entry'),
            ('both', 'Both'),
        ), 
        default='file'
    )
    
    # New fields
    is_group_assignment = models.BooleanField(default=False)
    max_attempts = models.PositiveSmallIntegerField(default=1)
    solution_file = models.FileField(upload_to='assignment_solutions/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.title} - {self.course}"

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        limit_choices_to={'user_type': 3}
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    text_entry = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='submissions/%Y/%m/%d/', null=True, blank=True)
    grade = models.PositiveSmallIntegerField(null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)
    is_late = models.BooleanField(default=False)
    
    # New fields
    attempt_number = models.PositiveSmallIntegerField(default=1)
    grader = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        blank=True,
        related_name='graded_submissions'
    )
    graded_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('assignment', 'student', 'attempt_number')
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"{self.student}'s submission for {self.assignment}"

class Exam(models.Model):
    EXAM_TYPE_CHOICES = (
        ('midterm', 'Midterm Exam'),
        ('final', 'Final Exam'),
        ('quiz', 'Quiz'),
        ('project', 'Project'),
    )
    course = models.ForeignKey(TermCourse, on_delete=models.CASCADE, related_name='exams')
    exam_type = models.CharField(max_length=10, choices=EXAM_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    date = models.DateTimeField()
    total_points = models.PositiveSmallIntegerField()
    weight = models.PositiveSmallIntegerField(
        help_text="Weight in percentage",
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    location = models.CharField(max_length=100, null=True, blank=True)
    
    # New fields
    duration = models.PositiveSmallIntegerField(
        help_text="Duration in minutes",
        null=True,
        blank=True
    )
    instructions = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.get_exam_type_display()} - {self.course}"

class Grade(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        limit_choices_to={'user_type': 3}
    )
    score = models.PositiveSmallIntegerField()
    comments = models.TextField(null=True, blank=True)
    published = models.BooleanField(default=False)
    
    # New fields
    curve_adjustment = models.SmallIntegerField(default=0)
    grading_scale = models.JSONField(null=True, blank=True)
    
    class Meta:
        unique_together = ('exam', 'student')
    
    # Validation
    def clean(self):
        if self.score > self.exam.total_points:
            raise ValidationError("Score cannot exceed exam's total points")
    
    def __str__(self):
        return f"{self.student}'s grade for {self.exam}"

