from django.utils import timezone
from rest_framework import serializers
from assessment.models import Assignment, Submission, Exam, Grade
from notifications.models import Announcement, AnnouncementAttachment
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
    class Meta:
        model = AnnouncementAttachment
        fields = ['announcement','file','original_filename','uploaded_at']


class AttendanceSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.course.name', read_only=True)

    class Meta:
        model = Attendance
        fields = ['id', 'date', 'status', 'course', 'course_name', 'notes']
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
