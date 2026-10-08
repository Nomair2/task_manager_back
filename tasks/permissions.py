from rest_framework.permissions import BasePermission
from workspaces.models import WorkspaceMembership



class CanCreateTask(BasePermission):
    def has_permission(self, request, view):

        message =   "You must be a workspace member to create task ."
        

        workspace_id = view.kwargs().get("workspace_id")

        return WorkspaceMembership.objects.filter(
            workspace_id= workspace_id , 
            user = request.user 
        ).exists()

class IsTaskWorkspaceMember(BasePermission):
    message = "You must be a workspace member."

    def has_object_permission(self, request, view, obj):
        return WorkspaceMembership.objects.filter(
            workspace=obj.project.workspace,
            user=request.user,
        ).exists()


class CanUpdateTask(BasePermission):
    message = "You do not have permission to update this task."

    def has_object_permission(self, request, view, obj):
        return WorkspaceMembership.objects.filter(
            workspace=obj.project.workspace,
            user=request.user,
        ).exists()


class CanDeleteTask(BasePermission):
    message = "Only workspace owners and admins can delete tasks."

    def has_object_permission(self, request, view, obj):
        return WorkspaceMembership.objects.filter(
            workspace=obj.project.workspace,
            user=request.user,
            role__in=[
                WorkspaceMembership.Role.OWNER,
                WorkspaceMembership.Role.ADMIN,
            ],
        ).exists()


class CanAssignTask(BasePermission):
    message = "You do not have permission to assign this task."

    def has_object_permission(self, request, view, obj):
        return WorkspaceMembership.objects.filter(
            workspace=obj.project.workspace,
            user=request.user,
        ).exists()


class CanChangeTaskStatus(BasePermission):
    message = "You do not have permission to change task status."

    def has_object_permission(self, request, view, obj):
        return WorkspaceMembership.objects.filter(
            workspace=obj.project.workspace,
            user=request.user,
        ).exists()