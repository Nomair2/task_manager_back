from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Workspace , WorkspaceMembership 


User = get_user_model()

class WorkspaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Workspace
        fields = [
            "id",
            "name",
            "slug",
            "owner",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "owner",
            "created_at",
            "updated_at",
        ]

    def validate_name(self , value):
        value = value.strip()

        if not value :
            raise serializers.ValidationError(
                "workpace name cannot be empty"
            )
        return value 

    def validate_slug(self , value):
        value = value.strip().lower()

        if not value : 
            raise serializers.ValidationError(
                'workspace slug cannot be empty'
            )
        return value 


class WorkspaceMembershipSerializer(serializers.ModelSerializer):

    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="user",
        write_only=True,
    )

    class Meta():
        model = WorkspaceMembership 
        fields = [
            "id",
            "user_id",
            "role",
            "joined_at"
        ]

        read_only_fields = [
            "id",
            "joined_at",
        ]
    def validate_role(self, value):
        if value == WorkspaceMembership.Role.OWNER:
            raise serializers.ValidationError(
                "Owner role cannot be assigned here."
            )
        return value 