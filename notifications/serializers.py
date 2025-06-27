# serializers.py (announcement)
from rest_framework import serializers
from .models import Announcement, AnnouncementView, AnnouncementComment, AnnouncementAttachment
from django.urls import reverse

from users.models import User
from django.utils import timezone
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'profile_picture']

class AnnouncementAttachmentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    file_size = serializers.SerializerMethodField()
    
    def get_file_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.file.url)
    
    def get_file_size(self, obj):
        return obj.file.size
    
    class Meta:
        model = AnnouncementAttachment
        fields = ['id', 'original_filename', 'file_url', 'file_size', 'uploaded_at']

class AnnouncementCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    can_edit = serializers.SerializerMethodField()
    
    def get_can_edit(self, obj):
        request = self.context.get('request')
        return request and request.user == obj.user
    
    class Meta:
        model = AnnouncementComment
        fields = ['id', 'user', 'comment', 'created_at', 'updated_at', 'can_edit']
        read_only_fields = ['created_at', 'updated_at']

class AnnouncementViewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = AnnouncementView
        fields = ['user', 'viewed_at', 'acknowledged_at']

class AnnouncementSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    related_course_name = serializers.CharField(source='related_course.course.name', read_only=True)
    attachments = AnnouncementAttachmentSerializer(many=True, read_only=True)
    comments = AnnouncementCommentSerializer(many=True, read_only=True)
    views = serializers.SerializerMethodField()
    
    # User-specific status fields
    is_viewed = serializers.SerializerMethodField()
    is_acknowledged = serializers.SerializerMethodField()
    requires_your_acknowledgment = serializers.SerializerMethodField()
    can_edit = serializers.SerializerMethodField()
    
    def get_is_viewed(self, obj):
        user = self.context['request'].user
        return obj.views.filter(user=user).exists()
    
    def get_is_acknowledged(self, obj):
        user = self.context['request'].user
        view = obj.views.filter(user=user).first()
        return view.acknowledged_at if view else None
    
    def get_requires_your_acknowledgment(self, obj):
        user = self.context['request'].user
        return (
            obj.requires_acknowledgment and 
            not obj.views.filter(user=user, acknowledged_at__isnull=False).exists() and
            (not obj.acknowledgment_deadline or obj.acknowledgment_deadline > timezone.now())
        )
    
    def get_can_edit(self, obj):
        user = self.context['request'].user
        return user == obj.created_by or user.is_superuser
    
    def get_views(self, obj):
        # Only show view stats to announcement creators
        if self.context['request'].user == obj.created_by:
            return {
                'total_views': obj.views.count(),
                'total_acknowledged': obj.views.exclude(acknowledged_at__isnull=True).count(),
                'pending_users': User.objects.filter(
                    groups__in=obj.target_groups()
                ).exclude(
                    announcement_views__announcement=obj
                ).count()
            }
        return None
    
    class Meta:
        model = Announcement
        fields = [
            'id', 'title', 'content', 'created_by', 'created_at', 'updated_at',
            'target_audience', 'is_important', 'expiry_date', 'related_course',
            'related_course_name', 'priority', 'requires_acknowledgment',
            'acknowledgment_deadline', 'attachments', 'comments', 'views',
            'is_viewed', 'is_acknowledged', 'requires_your_acknowledgment', 'can_edit'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']

class CreateAnnouncementSerializer(serializers.ModelSerializer):
    attachments = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=False),
        required=False
    )
    
    class Meta:
        model = Announcement
        fields = [
            'title', 'content', 'target_audience', 'is_important',
            'expiry_date', 'related_course', 'priority',
            'requires_acknowledgment', 'acknowledgment_deadline', 'attachments'
        ]
    
    def create(self, validated_data):
        attachments = validated_data.pop('attachments', [])
        announcement = Announcement.objects.create(
            created_by=self.context['request'].user,
            **validated_data
        )
        
        for attachment in attachments:
            AnnouncementAttachment.objects.create(
                announcement=announcement,
                file=attachment,
                original_filename=attachment.name
            )
        
        return announcement

class AcknowledgeAnnouncementSerializer(serializers.Serializer):
    acknowledged = serializers.BooleanField(default=True)

class AnnouncementStatsSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    unread = serializers.IntegerField()
    pending_acknowledgment = serializers.IntegerField()
    high_priority = serializers.IntegerField()
    expired = serializers.IntegerField()