from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "email"

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if not email or not password:
            raise serializers.ValidationError(
                {"detail": "Email and password are required"}
            )

        data = super().validate({
            "email": email,
            "password": password
        })

        user = self.user
        data["role"] = user.role
        return data


             
from rest_framework import serializers
from .models import User

class EmployeeSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password', '123456')
        role = validated_data.get('role', 'EMPLOYEE')
        user = User.objects.create_user(
            email=validated_data['email'],
            password=password,
            role=role
        )
        return user

# view for user profile
from rest_framework import serializers
from .models import User

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "role",
            "last_login",
            "is_active",
        ]
