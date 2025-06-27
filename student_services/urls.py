from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StudentDashboardView,

    StudentAttendanceViewSet,

)

router = DefaultRouter()
router.register(r'attendance', StudentAttendanceViewSet, basename='student-attendance')


urlpatterns = [
    path('dashboard/', StudentDashboardView.as_view(), name='student-dashboard'),
    path('', include(router.urls)),
]

