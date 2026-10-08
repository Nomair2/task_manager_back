from rest_framework.permissions import BasePermission
from workspaces.models import WorkspaceMembership

class CanCreateProject(BasePermission):
    message = (
        "Only workspace owners or admins can create projects"
    )

    def has_permission(self, request, view):
        workspace_id = view.kwargs.get("workspace_id")
        return WorkspaceMembership.objects.filter(
            workspace_id=workspace_id , 
            user= request.user ,
            role__in=[
                WorkspaceMembership.Role.OWNER , 
                WorkspaceMembership.Role.ADMIN
            ],
        ).exists()


class CanUpdateProject(BasePermission):
    message = (
        "Only workspace owners and admins can update projects."
    )

    def has_object_permission(self, request, view, obj):
        return WorkspaceMembership.objects.filter(
            workspace = obj.workspace , 
            user = request.user ,
            role__in = [
                WorkspaceMembership.Role.ADMIN , 
                WorkspaceMembership.Role.OWNER
            ]
        ).exists()

class CanDeleteProject(BasePermission):
    message = (
        "Only the workspace owner can delete projects."
    )

    def has_object_permission(self, request, view, obj):
        return WorkspaceMembership.objects.filter(
            workspace= obj.workspace , 
            user = request.user ,
            role = WorkspaceMembership.Role.OWNER
        ).exists()