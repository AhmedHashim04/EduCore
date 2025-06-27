# serializers.py
from rest_framework import serializers
from assessment.models import Assignment, Submission, Exam
from notifications.models import Announcement, AnnouncementAttachment
from student_services.models import Enrollment, StudentProfile
from courses.models import TermCourse
from users.models import User
class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ['gpa', 'completed_credits', 'academic_status']

class UserSerializer(serializers.ModelSerializer):
    profile = StudentProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'profile']

class TermCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermCourse
        fields = ['id', 'course', 'semester', 'professor', 'capacity', 'enrolled_students']

class EnrollmentSerializer(serializers.ModelSerializer):
    student = UserSerializer()
    
    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'enrollment_date', 'grade', 'is_active']

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnouncementAttachment
        fields = '__all__'
        read_only_fields = [ 'uploaded_at']


class CourseAnalyticsSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()
    course_name = serializers.CharField()
    student_count = serializers.IntegerField()
    avg_grade = serializers.DecimalField(max_digits=5, decimal_places=2)
    assignment_completion = serializers.DecimalField(max_digits=5, decimal_places=1)
    attendance_rate = serializers.DecimalField(max_digits=5, decimal_places=1)