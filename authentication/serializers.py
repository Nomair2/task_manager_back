from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth.password_validation import (
    validate_password,
)

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True, 
    )

    password_confirm = serializers.CharField(
        write_only=True,
    )

    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "password",
            "password_confirm",
        ]

    def validate(self ,attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError(
                {
                    "password":"Passwords do not match."
                }
            )
        validate_password(
            attrs['password']
        )
        return attrs 

    def validate_email(self, value):
        return value.strip().lower()

    def create(self , validated_data):
        validated_data.pop("password_confirm")

        password = validated_data.pop("password")

        user = User.objects.create_user(
            password=password ,
            **validated_data
        )

        return user 


class LoginSerializer(TokenObtainPairSerializer):
    username_field  = 'email' 

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        try:
            self.token = RefreshToken(attrs["refresh"])
        except TokenError:
            raise serializers.ValidationError(
                {
                    "refresh": "Invalid or expired refresh token."
                }
            )

        return attrs

    def save(self, **kwargs):
        self.token.blacklist()

class CurrentUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "email",
            "created_at",
            "updated_at",
        ]