from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.db.models import Q, Prefetch
from django.utils import timezone
from .models import Conversation, Participant, Message, MessageStatus
from .serializers import (
    ConversationSerializer, 
    MessageSerializer, 
    ParticipantSerializer
)
from users.models import User
class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    queryset = Conversation.objects.all()
    
    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(
            participants__user=user
        ).prefetch_related(
            Prefetch('participants', queryset=Participant.objects.select_related('user')),
            Prefetch('messages', queryset=Message.objects.order_by('-timestamp')[:1])
        ).distinct().order_by('-last_active')
    
    def get_serializer_context(self):
        return {'request': self.request}
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        conversation = self.get_object()
        participant = Participant.objects.get(
            conversation=conversation,
            user=request.user
        )
        participant.last_read = timezone.now()
        participant.save()
        
        # Update message statuses
        unread_messages = Message.objects.filter(
            conversation=conversation,
            timestamp__lte=timezone.now()
        ).exclude(sender=request.user)
        
        for message in unread_messages:
            status, created = MessageStatus.objects.get_or_create(
                message=message,
                user=request.user,
                defaults={'read': True, 'read_at': timezone.now()}
            )
            if not created and not status.read:
                status.read = True
                status.read_at = timezone.now()
                status.save()
        
        return Response({'status': 'conversation marked as read'})
    
    @action(detail=False, methods=['get'])
    def direct(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response(
                {'error': 'user_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            other_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Find or create direct conversation
        conversation = Conversation.objects.filter(
            type='direct',
            participants__user=request.user
        ).filter(
            participants__user=other_user
        ).distinct().first()
        
        if not conversation:
            conversation = Conversation.objects.create(type='direct')
            Participant.objects.create(
                conversation=conversation, 
                user=request.user
            )
            Participant.objects.create(
                conversation=conversation, 
                user=other_user
            )
        
        serializer = self.get_serializer(conversation)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def course_chats(self, request):
        course_id = request.query_params.get('course_id')
        if not course_id:
            return Response(
                {'error': 'course_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        conversations = Conversation.objects.filter(
            type='course',
            course_id=course_id,
            participants__user=request.user
        )
        serializer = self.get_serializer(conversations, many=True)
        return Response(serializer.data)

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_id')
        return Message.objects.filter(
            conversation_id=conversation_id
        ).select_related(
            'sender', 'reply_to'
        ).prefetch_related(
            'statuses'
        ).order_by('timestamp')
    
    def perform_create(self, serializer):
        conversation_id = self.kwargs.get('conversation_id')
        conversation = Conversation.objects.get(id=conversation_id)
        
        # Verify user is participant
        if not Participant.objects.filter(
            conversation=conversation,
            user=self.request.user
        ).exists():
            return Response(
                {'error': 'You are not a participant in this conversation'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        message = serializer.save(
            conversation=conversation,
            sender=self.request.user
        )
        
        # Update conversation activity
        conversation.last_active = timezone.now()
        conversation.save()
        
        # Create initial message statuses
        participants = Participant.objects.filter(
            conversation=conversation
        ).exclude(user=self.request.user)
        
        statuses = [
            MessageStatus(message=message, user=participant.user)
            for participant in participants
        ]
        MessageStatus.objects.bulk_create(statuses)
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, conversation_id=None, pk=None):
        message = self.get_object()
        status, created = MessageStatus.objects.get_or_create(
            message=message,
            user=request.user,
            defaults={'read': True, 'read_at': timezone.now()}
        )
        if not created and not status.read:
            status.read = True
            status.read_at = timezone.now()
            status.save()
        
        return Response({'status': 'message marked as read'})
    
    @action(detail=True, methods=['delete'])
    def delete_for_me(self, request, conversation_id=None, pk=None):
        message = self.get_object()
        if message.sender != request.user:
            return Response(
                {'error': 'You can only delete your own messages'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Soft delete implementation would go here
        # For now, just delete the message
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ParticipantViewSet(viewsets.ModelViewSet):
    serializer_class = ParticipantSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_id')
        return Participant.objects.filter(
            conversation_id=conversation_id
        ).select_related('user')
    
    def perform_create(self, serializer):
        conversation_id = self.kwargs.get('conversation_id')
        conversation = Conversation.objects.get(id=conversation_id)
        
        # Only allow admins to add participants
        admin_participant = Participant.objects.get(
            conversation=conversation,
            user=self.request.user
        )
        if not admin_participant.is_admin:
            return Response(
                {'error': 'Only conversation admins can add participants'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer.save(conversation=conversation)
        
        # Add welcome message
        new_user = serializer.validated_data['user']
        Message.objects.create(
            conversation=conversation,
            sender=self.request.user,
            content=f"{new_user.get_full_name()} has been added to the conversation"
        )
    
    def destroy(self, request, *args, **kwargs):
        participant = self.get_object()
        conversation = participant.conversation
        
        # Check permissions
        admin_participant = Participant.objects.get(
            conversation=conversation,
            user=request.user
        )
        if not admin_participant.is_admin and request.user != participant.user:
            return Response(
                {'error': 'You do not have permission to remove this participant'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Don't allow removal from direct chats
        if conversation.type == 'direct':
            return Response(
                {'error': 'Cannot remove participants from direct messages'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Add leave message
        if request.user == participant.user:
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=f"{request.user.get_full_name()} has left the conversation"
            )
        else:
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=f"{participant.user.get_full_name()} has been removed from the conversation"
            )
        
        participant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)