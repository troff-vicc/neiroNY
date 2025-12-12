from rest_framework.serializers import ModelSerializer
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from ..models import User


class UserSerializer(ModelSerializer):
    """Сериализатор для просмотра пользователя"""
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name')


class UserCreateSerializer(ModelSerializer):
    """Сериализатор для создания пользователя"""
    
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name')
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """Сериализатор для входа"""
    
    email = serializers.EmailField()
    password = serializers.CharField()