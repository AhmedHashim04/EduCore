
from rest_framework import serializers
from .models import TermCourse

class CourseSerializer(serializers.ModelSerializer):
    professor_name = serializers.CharField(source='professor.get_full_name', read_only=True)
    
    class Meta:
        model = TermCourse
        fields = ['id', 'course', 'semester', 'professor', 'professor_name', 'capacity']


class CourseEnrollmentSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()
    
    def validate_course_id(self, value):
        if not TermCourse.objects.filter(id=value).exists():
            raise serializers.ValidationError("Course does not exist")
        return value