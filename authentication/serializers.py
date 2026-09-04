from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=8,
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
        return attrs 

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