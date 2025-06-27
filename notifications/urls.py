# urls.py (announcement)
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnnouncementViewSet, AnnouncementCommentViewSet

router = DefaultRouter()
router.register(r'announcements', AnnouncementViewSet, basename='announcement')

comment_router = DefaultRouter()
comment_router.register(r'comments', AnnouncementCommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('announcements/<int:announcement_pk>/', include(comment_router.urls)),
    
    # Additional endpoints
    path('announcements/<int:pk>/acknowledge/', 
         AnnouncementViewSet.as_view({'post': 'acknowledge'}), 
         name='announcement-acknowledge'),
    path('announcements/<int:pk>/stats/', 
         AnnouncementViewSet.as_view({'get': 'view_stats'}), 
         name='announcement-stats'),
    path('announcements/stats/', 
         AnnouncementViewSet.as_view({'get': 'stats'}), 
         name='announcements-stats'),
]