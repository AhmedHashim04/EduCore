from rest_framework import serializers
from .models import  TermCourse, CourseMaterial
from .permissions import IsCourseStaff 

class CourseMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseMaterial
        fields = ['id', 'title', 'file', 'created_at']

class TermCourseSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()
    semester = serializers.SerializerMethodField()
    instructor = serializers.SerializerMethodField()
    materials = CourseMaterialSerializer(many=True, read_only=True)
    class Meta:
        model = TermCourse
        fields = '__all__'

    def get_course(self, obj):
        return {
            "id": obj.course.id,
            "code": obj.course.code,
            "title": obj.course.title,
        }

    def get_semester(self, obj):
        return {
            "id": obj.semester.id,
            "name": obj.semester.name,
        }

    def get_instructor(self, obj):
        if obj.instructor:
            return {
                "id": obj.instructor.id,
                "username": obj.instructor.username,
                "full_name": f"{obj.instructor.first_name} {obj.instructor.last_name}",
            }
        return None


    def update(self, instance, validated_data):
        # extract nested materials
        if IsCourseStaff:
            materials_data = self.initial_data.get('materials', [])
            # you can optionally clear old materials
            CourseMaterial.objects.filter(course=instance).delete()

            for material_data in materials_data:
                CourseMaterial.objects.create(course=instance, **material_data)

            return super().update(instance, validated_data)
        
        else :
            return {
                "error": "You are not authorized to update this course"
                }