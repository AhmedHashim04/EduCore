from django.db import models
from users.models import User
from django.core.exceptions import ValidationError
class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    target_audience = models.CharField(
        max_length=20, 
        choices=(
            ('all', 'All Users'),
            ('students', 'Students Only'),
            ('professors', 'Professors Only'),
            ('staff', 'Staff Only'),
            ('course', 'Specific Course'),
        ), 
        default='all'
    )
    is_important = models.BooleanField(default=False)
    expiry_date = models.DateTimeField(null=True, blank=True)
    related_course = models.ForeignKey(
        'courses.TermCourse', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    
    class Meta:
        ordering = ['-is_important', '-created_at']
    
    def __str__(self):
        return self.title

class AnnouncementWatch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)


class Resource(models.Model):
    RESOURCE_TYPE_CHOICES = (
        ('book', 'Book'), ('slide', 'Slide'), ('video', 'Video'),
        ('article', 'Article'), ('assignment', 'Assignment'),
        ('exam', 'Exam'), ('other', 'Other'),
    )
    course = models.ForeignKey(
        'courses.TermCourse', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    title = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPE_CHOICES)
    file = models.FileField(upload_to='resources/%Y/%m/%d/', null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False)
    
    # New fields
    version = models.PositiveSmallIntegerField(default=1)
    access_level = models.CharField(
        max_length=10,
        choices=(
            ('student', 'Students'),
            ('ta', 'Teaching Assistants'),
            ('instructor', 'Instructors Only'),
        ),
        default='student'
    )
    
    # Validation
    def clean(self):
        if not self.file and not self.url:
            raise ValidationError("Either file or URL must be provided")
    
    def __str__(self):
        return self.title