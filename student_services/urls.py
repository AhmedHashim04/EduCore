from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StudentDashboardView,

    StudentAttendanceViewSet,
    AnnouncementViewSet,
    StudentResourceViewSet
)

router = DefaultRouter()
router.register(r'attendance', StudentAttendanceViewSet, basename='student-attendance')
router.register(r'announcements', AnnouncementViewSet, basename='student-announcement')
router.register(r'resources', StudentResourceViewSet, basename='student-resource')

urlpatterns = [
    path('dashboard/', StudentDashboardView.as_view(), name='student-dashboard'),
    path('', include(router.urls)),
]

