from rest_framework import serializers
from .models import ProfessorProfile
from academics.serializers import DepartmentSerializer
from users.serializers import UserSerializer

class ProfessorProfileSerializer(serializers.ModelSerializer):
    professor = UserSerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)
    
    class Meta:
        model = ProfessorProfile
        fields = '__all__'