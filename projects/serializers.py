from rest_framework import serializers

from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id",
            "workspace",
            "name",
            "slug",
            "description",
            "created_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "workspace",
            "created_by",
            "created_at",
            "updated_at",
        ]

    def validate_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Project name cannot be empty."
            )

        return value

    def validate_slug(self, value):
        value = value.strip().lower()

        if not value:
            raise serializers.ValidationError(
                "Project slug cannot be empty."
            )

        return value