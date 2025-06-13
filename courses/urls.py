from django.urls import path
from .views import (
    CourseListView, CourseDetailView,
    CourseOfferingListView, CourseOfferingDetailView
)

urlpatterns = [
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('offerings/', CourseOfferingListView.as_view(), name='offering-list'),
    path('offerings/<int:pk>/', CourseOfferingDetailView.as_view(), name='offering-detail'),
]