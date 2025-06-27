# serializers.py
from rest_framework import serializers
from .models import (
    User, TermCourse, Assignment, 
    Exam, Submission, Grade
)
from django.utils import timezone

class ProfessorSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'

class ProfessorAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class ProfessorExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'


class StudentAssignmentSerializer(serializers.ModelSerializer):
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

class StudentExamSerializer(serializers.ModelSerializer):
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


class StudentSubmissionSerializer(serializers.ModelSerializer):
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

class StudentGradeSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='exam.course.course.name', read_only=True)
    exam_title = serializers.CharField(source='exam.title', read_only=True)
    max_score = serializers.IntegerField(source='exam.total_points', read_only=True)
    
    class Meta:
        model = Grade
        fields = [
            'id', 'exam', 'exam_title', 'course_name', 
            'score', 'max_score', 'comments', 'published'
        ]

