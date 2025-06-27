from django.db import models
from academics.models import Department, Semester
from users.models import User

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
    professor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,limit_choices_to={'user_type': 2})
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
    
