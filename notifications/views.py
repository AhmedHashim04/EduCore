from rest_framework import generics, permissions
from .models import Announcement, Resource
from .serializers import AnnouncementSerializer, ResourceSerializer
from django_filters.rest_framework import DjangoFilterBackend

class AnnouncementListView(generics.ListCreateAPIView):
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['target_audience', 'is_important']

    def get_queryset(self):
        user = self.request.user
        queryset = Announcement.objects.all()
        
        # Filter based on user type and target audience
        if user.user_type == 3:  # Student
            queryset = queryset.filter(target_audience__in=['all', 'students'])
        elif user.user_type == 2:  # Professor
            queryset = queryset.filter(target_audience__in=['all', 'professors'])
        elif user.user_type == 4:  # Staff
            queryset = queryset.filter(target_audience__in=['all', 'staff'])
            
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class AnnouncementDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated]

class ResourceListView(generics.ListCreateAPIView):
    serializer_class = ResourceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['course_offering', 'resource_type', 'is_public']

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

class ResourceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [permissions.IsAuthenticated]