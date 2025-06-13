from rest_framework import serializers
from .models import Enrollment, StudentProfile, Attendance
from courses.serializers import CourseOfferingSerializer
from academics.serializers import ProgramSerializer
from users.serializers import UserSerializer

class EnrollmentSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    course_offering = CourseOfferingSerializer(read_only=True)
    
    class Meta:
        model = Enrollment
        fields = '__all__'

class StudentProfileSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    program = ProgramSerializer(read_only=True)
    advisor = UserSerializer(read_only=True)
    
    class Meta:
        model = StudentProfile
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    course_offering = CourseOfferingSerializer(read_only=True)
    
    class Meta:
        model = Attendance
        fields = '__all__'