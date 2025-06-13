from rest_framework import serializers
from .models import Assignment, Submission, Exam, Grade
from courses.serializers import CourseOfferingSerializer
from users.serializers import UserSerializer

class AssignmentSerializer(serializers.ModelSerializer):
    course_offering = CourseOfferingSerializer(read_only=True)
    
    class Meta:
        model = Assignment
        fields = '__all__'

class SubmissionSerializer(serializers.ModelSerializer):
    assignment = AssignmentSerializer(read_only=True)
    student = UserSerializer(read_only=True)
    
    class Meta:
        model = Submission
        fields = '__all__'

class ExamSerializer(serializers.ModelSerializer):
    course_offering = CourseOfferingSerializer(read_only=True)
    
    class Meta:
        model = Exam
        fields = '__all__'

class GradeSerializer(serializers.ModelSerializer):
    exam = ExamSerializer(read_only=True)
    student = UserSerializer(read_only=True)
    
    class Meta:
        model = Grade
        fields = '__all__'