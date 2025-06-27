# views.py (announcement)
from rest_framework import viewsets, generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q, Count, F
from django.utils import timezone
from django_filters import rest_framework as filters
from .models import Announcement, AnnouncementView, AnnouncementComment
from .serializers import (
    AnnouncementSerializer, CreateAnnouncementSerializer,
    AnnouncementCommentSerializer, AcknowledgeAnnouncementSerializer,
    AnnouncementStatsSerializer
)

from  rest_framework.exceptions import PermissionDenied
class AnnouncementFilter(filters.FilterSet):
    priority = filters.NumberFilter(field_name='priority')
    requires_acknowledgment = filters.BooleanFilter(field_name='requires_acknowledgment')
    unread = filters.BooleanFilter(method='filter_unread')
    unacknowledged = filters.BooleanFilter(method='filter_unacknowledged')
    course = filters.NumberFilter(field_name='related_course_id')
    audience = filters.CharFilter(field_name='target_audience')
    
    def filter_unread(self, queryset, name, value):
        if value:
            user = self.request.user
            return queryset.exclude(views__user=user)
        return queryset
    
    def filter_unacknowledged(self, queryset, name, value):
        if value:
            user = self.request.user
            return queryset.filter(
                requires_acknowledgment=True
            ).exclude(
                views__user=user, 
                views__acknowledged_at__isnull=False
            )
        return queryset
    
    class Meta:
        model = Announcement
        fields = ['priority', 'requires_acknowledgment', 'unread', 'unacknowledged', 'course', 'audience']

class AnnouncementViewSet(viewsets.ModelViewSet):
    serializer_class = AnnouncementSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = AnnouncementFilter
    
    def get_queryset(self):
        user = self.request.user
        now = timezone.now()
        
        # Base queryset with prefetching
        queryset = Announcement.objects.filter(
            Q(expiry_date__isnull=True) | Q(expiry_date__gte=now)
        ).prefetch_related(
            'attachments', 'comments', 'views'
        ).select_related(
            'created_by', 'related_course', 'related_course__course'
        ).order_by('-priority', '-created_at')
        
        # Filter based on target audience
        if user.user_type == 1:  # Admin
            return queryset
        
        # Professor
        elif user.user_type == 2:
            return queryset.filter(
                Q(target_audience='all') |
                Q(target_audience='professors') |
                Q(related_course__professor=user) |
                Q(related_course__department__head_of_department=user)
            ).distinct()
        
        # Student
        elif user.user_type == 3:
            return queryset.filter(
                Q(target_audience='all') |
                Q(target_audience='students') |
                Q(related_course__enrollment__student=user)
            ).distinct()
        
        # Staff
        elif user.user_type == 4:
            return queryset.filter(
                Q(target_audience='all') |
                Q(target_audience='staff')
            ).distinct()
        
        return Announcement.objects.none()
    
    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return CreateAnnouncementSerializer
        return AnnouncementSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        
        # Mark as viewed
        view, created = AnnouncementView.objects.get_or_create(
            announcement=instance,
            user=user
        )
        if created:
            view.viewed_at = timezone.now()
            view.save()
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def acknowledge(self, request, pk=None):
        announcement = self.get_object()
        user = request.user
        
        if not announcement.requires_acknowledgment:
            return Response(
                {"error": "This announcement doesn't require acknowledgment"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        view, created = AnnouncementView.objects.get_or_create(
            announcement=announcement,
            user=user
        )
        
        serializer = AcknowledgeAnnouncementSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        if serializer.validated_data['acknowledged']:
            view.acknowledged_at = timezone.now()
            view.save()
            return Response({"status": "acknowledged"})
        
        view.acknowledged_at = None
        view.save()
        return Response({"status": "unacknowledged"})
    
    @action(detail=True, methods=['get'])
    def view_stats(self, request, pk=None):
        announcement = self.get_object()
        if announcement.created_by != request.user and not request.user.is_superuser:
            return Response(
                {"error": "You don't have permission to view these stats"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get detailed view stats
        views = announcement.views.select_related('user')
        acknowledged = views.exclude(acknowledged_at__isnull=True)
        
        # Get target audience
        if announcement.target_audience == 'course' and announcement.related_course:
            enrolled_users = announcement.related_course.enrollment_set.filter(
                is_active=True
            ).values_list('student', flat=True)
            target_users = User.objects.filter(id__in=enrolled_users)
        else:
            # Simplified for other audiences
            if announcement.target_audience == 'all':
                target_users = User.objects.all()
            else:
                target_users = User.objects.filter(user_type={
                    'students': 3,
                    'professors': 2,
                    'staff': 4
                }.get(announcement.target_audience, 1))
        
        pending_users = target_users.exclude(
            announcement_views__announcement=announcement
        )
        
        data = {
            'total_views': views.count(),
            'total_acknowledged': acknowledged.count(),
            'pending_users_count': pending_users.count(),
            'viewed_users': UserSerializer(
                [v.user for v in views], 
                many=True,
                context={'request': request}
            ).data,
            'pending_users': UserSerializer(
                pending_users, 
                many=True,
                context={'request': request}
            ).data[:50]  # Limit to first 50
        }
        
        return Response(data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        user = request.user
        now = timezone.now()
        
        queryset = self.get_queryset()
        total = queryset.count()
        
        # Unread announcements (not viewed by user)
        unread = queryset.exclude(views__user=user).count()
        
        # Pending acknowledgment
        pending_ack = queryset.filter(
            requires_acknowledgment=True,
            views__user=user,
            views__acknowledged_at__isnull=True
        ).count()
        
        # High priority announcements
        high_priority = queryset.filter(priority__gte=3).count()
        
        # Expired announcements (admin only)
        expired = 0
        if user.user_type == 1:  # Admin
            expired = Announcement.objects.filter(
                expiry_date__lt=now
            ).count()
        
        data = {
            'total': total,
            'unread': unread,
            'pending_acknowledgment': pending_ack,
            'high_priority': high_priority,
            'expired': expired
        }
        
        serializer = AnnouncementStatsSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

class AnnouncementCommentViewSet(viewsets.ModelViewSet):
    serializer_class = AnnouncementCommentSerializer
    
    def get_queryset(self):
        return AnnouncementComment.objects.filter(
            announcement_id=self.kwargs['announcement_pk']
        ).select_related('user').order_by('created_at')
    
    def perform_create(self, serializer):
        announcement = Announcement.objects.get(pk=self.kwargs['announcement_pk'])
        serializer.save(
            user=self.request.user,
            announcement=announcement
        )
    
    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise PermissionDenied("You can only edit your own comments")
        serializer.save()
    
    def perform_destroy(self, instance):
        if instance.user != self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied("You can only delete your own comments")
        instance.delete()