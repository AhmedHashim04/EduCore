from rest_framework import generics, permissions
from .models import  TermCourse
from .serializers import  TermCourseSerializer
from academics.models import Semester
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsCourseInstructor, IsCourseStudent, IsCourseStaff
