# urls.py (student)
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StudentDashboardView,
    StudentCourseViewSet,
    StudentAssignmentViewSet,
    StudentSubmissionViewSet,
    StudentEnrollmentViewSet,
    StudentGradeViewSet,
    StudentAttendanceViewSet,
    AnnouncementViewSet,
    StudentResourceViewSet
)

router = DefaultRouter()
router.register(r'courses', StudentCourseViewSet, basename='student-course')
router.register(r'assignments', StudentAssignmentViewSet, basename='student-assignment')
router.register(r'submissions', StudentSubmissionViewSet, basename='student-submission')
router.register(r'grades', StudentGradeViewSet, basename='student-grade')
router.register(r'attendance', StudentAttendanceViewSet, basename='student-attendance')
router.register(r'announcements', AnnouncementViewSet, basename='student-announcement')
router.register(r'resources', StudentResourceViewSet, basename='student-resource')

urlpatterns = [
    path('dashboard/', StudentDashboardView.as_view(), name='student-dashboard'),
    path('enrollment/', StudentEnrollmentViewSet.as_view({
        'post': 'enroll'
    }), name='student-enroll'),
    path('enrollment/<int:pk>/withdraw/', StudentEnrollmentViewSet.as_view({
        'post': 'withdraw'
    }), name='student-withdraw'),
    path('', include(router.urls)),
]