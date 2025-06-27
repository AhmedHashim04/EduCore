from rest_framework import serializers
from .models import Conversation, Participant, Message, MessageStatus
from django.contrib.auth import get_user_model

from datetime import timedelta
from django.utils import timezone

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    online_status = serializers.SerializerMethodField()
    
    def get_online_status(self, obj):
        # This would connect to your presence system
        return "online" if obj.last_activity > timezone.now() - timedelta(minutes=5) else "offline"
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'profile_picture', 'online_status']

class ParticipantSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    unread_count = serializers.SerializerMethodField()
    
    def get_unread_count(self, obj):
        if obj.last_read:
            return Message.objects.filter(
                conversation=obj.conversation,
                timestamp__gt=obj.last_read
            ).exclude(sender=obj.user).count()
        return Message.objects.filter(conversation=obj.conversation).exclude(sender=obj.user).count()
    
    class Meta:
        model = Participant
        fields = ['id', 'user', 'joined_at', 'last_read', 'is_admin', 'unread_count']

class MessageStatusSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = MessageStatus
        fields = ['user', 'read', 'read_at']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    statuses = MessageStatusSerializer(many=True, read_only=True)
    reply_to = serializers.PrimaryKeyRelatedField(queryset=Message.objects.all(), required=False)
    attachment_url = serializers.SerializerMethodField()
    is_edited = serializers.BooleanField(source='edited', read_only=True)
    
    def get_attachment_url(self, obj):
        if obj.attachment:
            return self.context['request'].build_absolute_uri(obj.attachment.url)
        return None
    
    class Meta:
        model = Message
        fields = [
            'id', 'conversation', 'sender', 'content', 'timestamp', 
            'read_by', 'reply_to', 'attachment', 'attachment_type',
            'attachment_url', 'edited', 'edited_at', 'statuses', 'is_edited'
        ]
        read_only_fields = ['timestamp', 'read_by', 'edited', 'edited_at']

class ConversationSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    is_direct = serializers.BooleanField(source='is_direct_chat', read_only=True)
    
    def get_last_message(self, obj):
        last_msg = obj.messages.last()
        return MessageSerializer(last_msg, context=self.context).data if last_msg else None
    
    def get_unread_count(self, obj):
        user = self.context['request'].user
        participant = Participant.objects.filter(conversation=obj, user=user).first()
        if participant and participant.last_read:
            return obj.messages.filter(timestamp__gt=participant.last_read).exclude(sender=user).count()
        return obj.messages.exclude(sender=user).count()
    
    def create(self, validated_data):
        participants = self.initial_data.get('participants', [])
        conv_type = validated_data.get('type', 'direct')
        
        # Create conversation
        conversation = Conversation.objects.create(**validated_data)
        
        # Add participants
        for user_id in participants:
            user = User.objects.get(id=user_id)
            is_admin = (user.user_type in [1, 2])  # Admins and professors are admins
            Participant.objects.create(
                conversation=conversation,
                user=user,
                is_admin=is_admin
            )
        
        return conversation
    
    class Meta:
        model = Conversation
        fields = [
            'id', 'type', 'course', 'group_name', 'created_at', 
            'last_active', 'participants', 'last_message', 
            'unread_count', 'is_direct'
        ]