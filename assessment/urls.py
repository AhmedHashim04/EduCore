# urls.py (student)
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AssignmentViewSet,
    ExamViewSet,
    GradeSubmissionView,
    StudentAssignmentViewSet,
    StudentSubmissionViewSet,
    StudentGradeViewSet,

)

router = DefaultRouter()
router.register(r'assignments', StudentAssignmentViewSet, basename='student-assignment')
router.register(r'submissions', StudentSubmissionViewSet, basename='student-submission')
router.register(r'grades', StudentGradeViewSet, basename='student-grade')
router.register('assignments/professor/', AssignmentViewSet, basename='professor-assignment')
router.register('exams/professor/', ExamViewSet, basename='professor-exam')


urlpatterns = [
    path('', include(router.urls)),
    path('grade-submission/<int:pk>/', GradeSubmissionView.as_view(), name='grade-submission'),
]


