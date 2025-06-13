from django.db import models
from users.models import User
from academics.models import Department

class ProfessorProfile(models.Model):
    professor = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 2})
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    position = models.CharField(max_length=100)
    office_location = models.CharField(max_length=100, null=True, blank=True)
    office_hours = models.CharField(max_length=200, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    research_interests = models.TextField(null=True, blank=True)
    hire_date = models.DateField()
    
    def __str__(self):
        return f"{self.professor}'s profile"