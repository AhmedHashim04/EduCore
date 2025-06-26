from django.utils import timezone
from rest_framework import serializers
from assessment.models import Assignment, Submission, Exam, Grade
from notifications.models import Announcement, Resource
from student_services.models import Enrollment, StudentProfile, Attendance
from courses.models import TermCourse


class CourseSerializer(serializers.ModelSerializer):
    professor_name = serializers.CharField(source='professor.get_full_name', read_only=True)
    
    class Meta:
        model = TermCourse
        fields = ['id', 'course', 'semester', 'professor', 'professor_name', 'capacity']

class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    
    class Meta:
        model = Enrollment
        fields = ['id', 'course', 'enrollment_date', 'grade', 'is_active']

class AssignmentSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.course.name', read_only=True)
    submission_status = serializers.SerializerMethodField()
    due_date_passed = serializers.SerializerMethodField()
    
    def get_submission_status(self, obj):
        student = self.context['request'].user
        submission = Submission.objects.filter(assignment=obj, student=student).first()
        if submission:
            return 'submitted' if submission.grade is None else 'graded'
        return 'not_submitted'
    
    def get_due_date_passed(self, obj):
        return timezone.now() > obj.due_date
    
    class Meta:
        model = Assignment
        fields = [
            'id', 'title', 'description', 'due_date', 'total_points', 
            'course', 'course_name', 'submission_type', 'submission_status',
            'due_date_passed'
        ]

class ExamSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.course.name', read_only=True)
    grade = serializers.SerializerMethodField()
    time_until = serializers.SerializerMethodField()
    
    def get_grade(self, obj):
        student = self.context['request'].user
        grade = Grade.objects.filter(exam=obj, student=student).first()
        return grade.score if grade and grade.published else None
    
    def get_time_until(self, obj):
        return obj.date - timezone.now()
    
    class Meta:
        model = Exam
        fields = [
            'id', 'exam_type', 'title', 'date', 'total_points', 
            'course', 'course_name', 'grade', 'time_until', 'location'
        ]

class ResourceSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.course.name', read_only=True)
    file_url = serializers.SerializerMethodField()
    
    def get_file_url(self, obj):
        if obj.file:
            return self.context['request'].build_absolute_uri(obj.file.url)
        return None
    
    class Meta:
        model = Resource
        fields = [
            'id', 'title', 'resource_type', 'description', 
            'course', 'course_name', 'file_url', 'url', 
            'uploaded_at', 'access_level'
        ]

class AnnouncementSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='related_course.course.name', read_only=True, allow_null=True)
    is_new = serializers.SerializerMethodField()
    
    def get_is_new(self, obj):
        student = self.context['request'].user
        last_view = student.announcement_views.filter(announcement=obj).first()
        return not last_view or last_view.viewed_at < obj.updated_at
    
    class Meta:
        model = Announcement
        fields = [
            'id', 'title', 'content', 'created_at', 
            'is_important', 'course_name', 'is_new'
        ]

class AttendanceSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.course.name', read_only=True)

    class Meta:
        model = Attendance
        fields = ['id', 'date', 'status', 'course', 'course_name', 'notes']

class SubmissionSerializer(serializers.ModelSerializer):
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)
    file_url = serializers.SerializerMethodField()
    
    def get_file_url(self, obj):
        if obj.file:
            return self.context['request'].build_absolute_uri(obj.file.url)
        return None
    
    class Meta:
        model = Submission
        fields = [
            'id', 'assignment', 'assignment_title', 'submitted_at', 
            'text_entry', 'file_url', 'grade', 'feedback', 
            'is_late', 'attempt_number'
        ]

class GradeSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='exam.course.course.name', read_only=True)
    exam_title = serializers.CharField(source='exam.title', read_only=True)
    max_score = serializers.IntegerField(source='exam.total_points', read_only=True)
    
    class Meta:
        model = Grade
        fields = [
            'id', 'exam', 'exam_title', 'course_name', 
            'score', 'max_score', 'comments', 'published'
        ]

class StudentProfileSerializer(serializers.ModelSerializer):
    program_name = serializers.CharField(source='program.name', read_only=True)
    advisor_name = serializers.CharField(source='advisor.get_full_name', read_only=True)
    
    class Meta:
        model = StudentProfile
        fields = [
            'program', 'program_name', 'enrollment_date', 
            'expected_graduation', 'current_semester', 
            'advisor', 'advisor_name', 'gpa', 
            'completed_credits', 'academic_status'
        ]

class CourseEnrollmentSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()
    
    def validate_course_id(self, value):
        if not TermCourse.objects.filter(id=value).exists():
            raise serializers.ValidationError("Course does not exist")
        return value