# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProfessorCourseViewSet,
    AnnouncementViewSet,
    ResourceViewSet,
)

router = DefaultRouter()
router.register('courses', ProfessorCourseViewSet, basename='professor-course')

router.register('announcements', AnnouncementViewSet, basename='professor-announcement')
router.register('resources', ResourceViewSet, basename='professor-resource')

urlpatterns = [
    path('', include(router.urls)),
    
    # Additional endpoints
    path('dashboard-summary/', ProfessorCourseViewSet.as_view({'get': 'list'}), name='dashboard-summary'),
]