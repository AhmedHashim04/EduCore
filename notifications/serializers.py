from rest_framework import serializers
from .models import Announcement, Resource
from users.serializers import UserSerializer
from courses.serializers import CourseOfferingSerializer

class AnnouncementSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Announcement
        fields = '__all__'

class ResourceSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializer(read_only=True)
    course_offering = CourseOfferingSerializer(read_only=True)
    
    class Meta:
        model = Resource
        fields = '__all__'