from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'conversations', views.ConversationViewSet, basename='conversation')
router.register(r'participants', views.ParticipantViewSet, basename='participant')

message_router = DefaultRouter()
message_router.register(r'messages', views.MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
    
    # Conversation-specific routes
    path('conversations/direct/', 
         views.ConversationViewSet.as_view({'get': 'direct'}), 
         name='direct-conversation'),
    path('conversations/course/', 
         views.ConversationViewSet.as_view({'get': 'course_chats'}), 
         name='course-conversations'),
    path('conversations/<int:pk>/mark_read/', 
         views.ConversationViewSet.as_view({'post': 'mark_read'}), 
         name='mark-conversation-read'),
    
    # Conversation message routes
    path('conversations/<int:conversation_id>/', include(message_router.urls)),
    path('conversations/<int:conversation_id>/messages/<int:pk>/mark_read/', 
         views.MessageViewSet.as_view({'post': 'mark_read'}), 
         name='mark-message-read'),
    path('conversations/<int:conversation_id>/messages/<int:pk>/delete_for_me/', 
         views.MessageViewSet.as_view({'delete': 'delete_for_me'}), 
         name='delete-message-for-me'),
    
    # Participant management
    path('conversations/<int:conversation_id>/participants/', 
         views.ParticipantViewSet.as_view({'get': 'list', 'post': 'create'}), 
         name='participant-list'),
    path('conversations/<int:conversation_id>/participants/<int:pk>/', 
         views.ParticipantViewSet.as_view({'delete': 'destroy'}), 
         name='participant-detail'),
]