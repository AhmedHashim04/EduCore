from django.db import models
from users.models import User
from django.core.exceptions import ValidationError

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    target_audience = models.CharField(max_length=20, choices=
                                        (('all', 'All Users'),('students', 'Students Only'),
                                        ('professors', 'Professors Only'),('staff', 'Staff Only'),
                                        ('course', 'Specific Course'),), default='all')
    is_important = models.BooleanField(default=False)
    expiry_date = models.DateTimeField(null=True, blank=True)
    related_course = models.ForeignKey('courses.TermCourse', on_delete=models.CASCADE, null=True, blank=True)
    priority = models.PositiveSmallIntegerField(
        choices=((1, 'Low'), (2, 'Medium'), (3, 'High'), (4, 'Critical')),
        default=2
    )
    requires_acknowledgment = models.BooleanField(default=False)
    acknowledgment_deadline = models.DateTimeField(null=True, blank=True)
    class Meta:
        ordering = ['-is_important', '-created_at']
    
    def __str__(self):
        return self.title

class AnnouncementView(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='announcement_views')
    viewed_at = models.DateTimeField(auto_now_add=True)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('announcement', 'user')
        
    def __str__(self):
        return f"{self.user} viewed {self.announcement}"

class AnnouncementComment(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
        
    def __str__(self):
        return f"Comment by {self.user} on {self.announcement}"

class AnnouncementAttachment(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='announcements/attachments/%Y/%m/%d/')
    original_filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Attachment for {self.announcement}"
    
    