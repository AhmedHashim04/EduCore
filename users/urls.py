from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    ProfileView,
    
)
import djoser
urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileView.as_view(), name='profile'),
]