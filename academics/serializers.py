from rest_framework import serializers
from .models import Department, Program, Semester
from users.serializers import UserSerializer

class DepartmentSerializer(serializers.ModelSerializer):
    head_of_department = UserSerializer(read_only=True)
    
    class Meta:
        model = Department
        fields = '__all__'

class ProgramSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    
    class Meta:
        model = Program
        fields = '__all__'

class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = '__all__'