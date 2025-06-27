from django.urls import path, include
from .views import (
    ProfileView
    
)
import djoser
urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    path('profile/', ProfileView.as_view(), name='profile'),
]