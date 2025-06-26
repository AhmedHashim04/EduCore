from django.urls import path
from .views import (
    ProfessorProfileListView,
    ProfessorProfileDetailView
)

urlpatterns = [
    path('profiles/', ProfessorProfileListView.as_view(), name='professor-profile-list'),
    path('profiles/<int:pk>/', ProfessorProfileDetailView.as_view(), name='professor-profile-detail'),
]