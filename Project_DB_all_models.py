from assessment.models import Assignment, Submission, Exam, Grade
from notifications.models import Announcement, AnnouncementView, AnnouncementComment, AnnouncementAttachment
from student_services.models import Enrollment, StudentProfile, Attendance
from professor_dashboard.models import ProfessorProfile
from academics.models import Department, Program, Semester
from courses.models import Course, TermCourse, CourseMaterial, Section
from chat.models import Conversation, Participant, Message, MessageStatus
from users.models import User

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

class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(null=True, blank=True)
    head_of_department = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        limit_choices_to={'user_type': 2}
    )
    established_date = models.DateField()
    website = models.URLField(null=True, blank=True)
    budget_code = models.CharField(max_length=20, null=True, blank=True)
    contact_email = models.EmailField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class Program(models.Model):
    DEGREE_CHOICES = (
        ('BSc', 'Bachelor of Science'), ('BA', 'Bachelor of Arts'),
        ('MSc', 'Master of Science'), ('MA', 'Master of Arts'),
        ('PhD', 'Doctor of Philosophy'), ('Cert', 'Certificate'),
    )
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    degree = models.CharField(max_length=10, choices=DEGREE_CHOICES)
    duration = models.PositiveSmallIntegerField(
        help_text="Duration in years",
        validators=[MinValueValidator(1), MaxValueValidator(6)]
    )
    description = models.TextField()
    total_credits = models.PositiveSmallIntegerField()
    
    # New fields
    accreditation_status = models.BooleanField(default=True)
    accreditation_expiry = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.get_degree_display()} in {self.name}"

class Semester(models.Model):
    SEMESTER_CHOICES = (
        ('Fall', 'Fall'), ('Spring', 'Spring'), ('Summer', 'Summer'),
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
    
    # Ensure only one current semester
    def save(self, *args, **kwargs):
        if self.is_current:
            Semester.objects.filter(is_current=True).update(is_current=False)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.get_semester_display()} {self.year}"

class Course(models.Model):
    code = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    description = models.TextField()
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True)
    is_core = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.code} - {self.title}"
    
    def __str__(self):
        return f"{self.course} - {self.semester}"

class TermCourse(models.Model):
    """
    Represents a specific offering of a course in a given semester.

    This model links a course to a semester, assigns an instructor, and 
    includes metadata such as section code, classroom, schedule, capacity,
    and enrollment count. Each TermCourse corresponds to a unique
    section of a course, allowing for multiple offerings of the same course
    in different sections, schedules, or instructors.
    """
    slug = models.SlugField(max_length=10, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    credits = models.PositiveSmallIntegerField()
    instructor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,limit_choices_to={'user_type': 2})
    sections = models.ManyToManyField('Section', blank=True)
    capacity = models.PositiveSmallIntegerField()
    schedule = models.CharField(max_length=100, help_text="e.g., Mon/Wed 10:00-11:30")
    classroom = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def add_slug(self):
        self.slug = f"{self.course.code}-in-{self.semester.semester}-{self.semester.year}"

    class Meta:
        # unique_together = ('course', 'semester', 'section')
        unique_together = ('schedule', 'classroom')
    
    def __str__(self):
        return f"{self.course.code} -{self.course.title} - ({self.semester})"
        # return f"{self.course.code} - {self.section} ({self.semester})"

class CourseMaterial(models.Model):
    course = models.ForeignKey(TermCourse, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to=f'{course}/materials/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - {self.course} - {self.course.instructor} - {self.course.semester}"

class Section(models.Model):
    staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,limit_choices_to={'user_type': 4})
    capacity = models.PositiveSmallIntegerField()
    schedule = models.CharField(max_length=100, help_text="e.g., Mon/Wed 10:00-11:30")
    classroom = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('schedule', 'classroom')
    
    def __str__(self):
        return f"{self.classroom} - {self.staff}"

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
