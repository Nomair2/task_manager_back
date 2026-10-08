from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Task
from workspaces.models import WorkspaceMembership

User = get_user_model()
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "project",
            "title",
            "description",
            "status",
            "priority",
            "creator",
            "assignee",
            "due_date",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "project",
            "creator",
            "created_at",
            "updated_at",
        ]

    def validate_title(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Task title cannot be empty."
            )

        return value

    def validate_assignee(self , value ):
        workspace = self.context.get("workspace")

        if workspace is None : 
            raise serializers.ValidationError("Workspace context is required.")

        is_member = WorkspaceMembership.objects.filter(
            workspace = workspace ,
            user = value
        ).exists()

        if not is_member:
            raise serializers.ValidationError(
                "Assignee must be a member of this workspace."
            )

        return value

    


class TaskAssignmentSerializer(serializers.Serializer):
    assignee = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        required= True ,
        allow_null=True ,
    )

    def validate_assignee(self , value ):
        workspace = self.context.get("workspace_id")

        if workspace is None :
            raise serializers.ValidationError(
                "Assignee must be a member of this workspace."
            )

        is_member = WorkspaceMembership.objects.filter(
            workspace = workspace , 
            user = value ,
        ).exists()

        if not is_member:
            raise serializers.ValidationError(
                "Assignee must be a member of this workspace."
            )

        return value 



class TaskStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(
        choices=Task.Status.choices,
    )