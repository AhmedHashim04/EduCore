from django.db import models
from users.models import User

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    target_audience = models.CharField(max_length=20, choices=(
        ('all', 'All Users'),
        ('students', 'Students Only'),
        ('professors', 'Professors Only'),
        ('staff', 'Staff Only'),
    ), default='all')
    is_important = models.BooleanField(default=False)
    expiry_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.title

class Resource(models.Model):
    RESOURCE_TYPE_CHOICES = (
        ('book', 'Book'),
        ('slide', 'Slide'),
        ('video', 'Video'),
        ('article', 'Article'),
        ('other', 'Other'),
    )
    
    course_offering = models.ForeignKey('courses.CourseOffering', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPE_CHOICES)
    file = models.FileField(upload_to='resources/', null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title