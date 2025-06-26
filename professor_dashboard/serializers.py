from rest_framework import serializers
from .models import ProfessorProfile
from academics.serializers import DepartmentSerializer
from users.serializers import CustomUserSerializer

class ProfessorProfileSerializer(serializers.ModelSerializer):
    professor = CustomUserSerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)
    
    class Meta:
        model = ProfessorProfile
        fields = '__all__'