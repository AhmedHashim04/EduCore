# urls.py (student)
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StudentCourseViewSet,

    StudentEnrollmentViewSet,

)

router = DefaultRouter()
router.register(r'courses', StudentCourseViewSet, basename='student-course')
urlpatterns = [
    path('enrollment/', StudentEnrollmentViewSet.as_view({'post': 'enroll'}), name='student-enroll'),
    path('enrollment/<int:pk>/withdraw/', StudentEnrollmentViewSet.as_view({'post': 'withdraw'}), name='student-withdraw'),
    path('', include(router.urls)),
]