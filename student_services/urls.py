from django.urls import path
from .views import (
    EnrollmentListView, EnrollmentDetailView,
    StudentProfileListView, StudentProfileDetailView,
    AttendanceListView, AttendanceDetailView
)

urlpatterns = [
    path('enrollments/', EnrollmentListView.as_view(), name='enrollment-list'),
    path('enrollments/<int:pk>/', EnrollmentDetailView.as_view(), name='enrollment-detail'),
    path('profiles/', StudentProfileListView.as_view(), name='profile-list'),
    path('profiles/<int:pk>/', StudentProfileDetailView.as_view(), name='profile-detail'),
    path('attendance/', AttendanceListView.as_view(), name='attendance-list'),
    path('attendance/<int:pk>/', AttendanceDetailView.as_view(), name='attendance-detail'),
]