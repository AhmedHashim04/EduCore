from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                    'user_type', 'profile_picture', 'phone_number', 'date_of_birth', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'user_type': {'default': 'student'}
        }

    def validate_user_type(self, value):
        if value == 'admin':
            raise serializers.ValidationError("You are not allowed to choose 'admin' as user type.")
        return value
    
    def validate_date_of_birth(self, value):
        if value > '2009-01-01':
            raise serializers.ValidationError("You must be at least 18 years old to register.")
        return value
    
    def validate_phone_number(self, value):
        if len(value) != 10:
            raise serializers.ValidationError("Phone number must be 10 digits.")
        if not value[0:3] in ['010', '011', '012', '015']:
            raise serializers.ValidationError("Phone number must be Egyptian (starting with 010, 011, 012, or 015).")
        return value
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user_type'] = user.user_type
        token['username'] = user.username
        return token

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                    'user_type', 'profile_picture', 'phone_number', 
                    'address', 'date_of_birth', 'bio']
        read_only_fields = ['id', 'username', 'user_type']