# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProfessorCourseViewSet,

)

router = DefaultRouter()
router.register('courses', ProfessorCourseViewSet, basename='professor-course')

urlpatterns = [
    path('', include(router.urls)),
    
    # Additional endpoints
    path('dashboard-summary/', ProfessorCourseViewSet.as_view({'get': 'list'}), name='dashboard-summary'),
]