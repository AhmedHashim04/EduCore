# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProfessorCourseViewSet,
    AssignmentViewSet,
    ExamViewSet,
    AnnouncementViewSet,
    ResourceViewSet,
    GradeSubmissionView
)

router = DefaultRouter()
router.register('courses', ProfessorCourseViewSet, basename='professor-course')
router.register('assignments', AssignmentViewSet, basename='professor-assignment')
router.register('exams', ExamViewSet, basename='professor-exam')
router.register('announcements', AnnouncementViewSet, basename='professor-announcement')
router.register('resources', ResourceViewSet, basename='professor-resource')

urlpatterns = [
    path('', include(router.urls)),
    path('grade-submission/<int:pk>/', GradeSubmissionView.as_view(), name='grade-submission'),
    
    # Additional endpoints
    path('dashboard-summary/', ProfessorCourseViewSet.as_view({'get': 'list'}), name='dashboard-summary'),
]