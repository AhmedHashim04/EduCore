from rest_framework import serializers
from .models import Enrollment, StudentProfile, Attendance
from courses.serializers import TermCourseSerializer
from academics.serializers import ProgramSerializer
from users.serializers import CustomUserSerializer

class EnrollmentSerializer(serializers.ModelSerializer):
    student = CustomUserSerializer(read_only=True)
    course = TermCourseSerializer(read_only=True)
    
    class Meta:
        model = Enrollment
        fields = '__all__'

class StudentProfileSerializer(serializers.ModelSerializer):
    student = CustomUserSerializer(read_only=True)
    program = ProgramSerializer(read_only=True)
    advisor = CustomUserSerializer(read_only=True)
    
    class Meta:
        model = StudentProfile
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    student = CustomUserSerializer(read_only=True)
    course = TermCourseSerializer(read_only=True)
    
    class Meta:
        model = Attendance
        fields = '__all__'