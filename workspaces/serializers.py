from rest_framework import serializers

from .models import Workspace


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