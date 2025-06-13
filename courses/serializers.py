from rest_framework import serializers
from .models import Course, CourseOffering
from academics.serializers import SemesterSerializer, DepartmentSerializer
from users.serializers import UserSerializer

class CourseSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    
    class Meta:
        model = Course
        fields = '__all__'

class CourseOfferingSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    semester = SemesterSerializer(read_only=True)
    instructor = UserSerializer(read_only=True)
    
    class Meta:
        model = CourseOffering
        fields = '__all__'