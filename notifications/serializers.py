from rest_framework import serializers
from .models import Announcement, Resource
from users.serializers import CustomUserSerializer
from courses.serializers import TermCourseSerializer

class AnnouncementSerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(read_only=True)
    
    class Meta:
        model = Announcement
        fields = '__all__'

class ResourceSerializer(serializers.ModelSerializer):
    uploaded_by = CustomUserSerializer(read_only=True)
    course_offering = TermCourseSerializer(read_only=True)
    
    class Meta:
        model = Resource
        fields = '__all__'