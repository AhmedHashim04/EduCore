from django.urls import path
from .views import (
    DepartmentListView, DepartmentDetailView,
    ProgramListView, ProgramDetailView,
    SemesterListView, SemesterDetailView
)

urlpatterns = [
    path('departments/', DepartmentListView.as_view(), name='department-list'),
    path('departments/<int:pk>/', DepartmentDetailView.as_view(), name='department-detail'),
    path('programs/', ProgramListView.as_view(), name='program-list'),
    path('programs/<int:pk>/', ProgramDetailView.as_view(), name='program-detail'),
    path('semesters/', SemesterListView.as_view(), name='semester-list'),
    path('semesters/<int:pk>/', SemesterDetailView.as_view(), name='semester-detail'),
]