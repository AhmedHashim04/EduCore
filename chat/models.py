from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Conversation(models.Model):
    CONVERSATION_TYPES = (
        ('direct', 'Direct Message'),
        ('course', 'Course Discussion'),
        ('group', 'Study Group'),
    )
    
    type = models.CharField(max_length=10, choices=CONVERSATION_TYPES, default='direct')
    course = models.ForeignKey('courses.TermCourse', on_delete=models.CASCADE, null=True, blank=True)
    group_name = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-last_active']
    
    def __str__(self):
        if self.type == 'direct':
            return f"Direct Chat: {self.participants.first()} & {self.participants.last()}"
        return self.group_name or f"Course: {self.course.course.name}"

class Participant(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    last_read = models.DateTimeField(null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('conversation', 'user')
        ordering = ['-joined_at']
    
    def __str__(self):
        return f"{self.user} in {self.conversation}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read_by = models.ManyToManyField(User, related_name='read_messages', blank=True)
    reply_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    
    # For file attachments
    attachment = models.FileField(upload_to='chat_attachments/%Y/%m/%d/', null=True, blank=True)
    attachment_type = models.CharField(
        max_length=20,
        choices=(('file', 'File'), ('image', 'Image'), ('video', 'Video')),
        null=True, 
        blank=True
    )
    
    # Message status tracking
    edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['timestamp']
        indexes = [
            models.Index(fields=['conversation', 'timestamp']),
        ]
    
    def __str__(self):
        return f"{self.sender} at {self.timestamp}: {self.content[:50]}"

class MessageStatus(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='statuses')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('message', 'user')
        verbose_name_plural = 'Message Statuses'
    
    def __str__(self):
        return f"{self.user} - {'Read' if self.read else 'Unread'}"