from rest_framework.permissions import BasePermission
from .models import WorkspaceMembership



class IsWorkspaceMember(BasePermission):
    """
    Allows access only to users who are members
    of the workspace.
    """

    def has_object_permission(
        self,
        request,
        view,
        obj,
    ):
        return WorkspaceMembership.objects.filter(
            workspace=obj,
            user=request.user,
        ).exists()


class IsWorkspaceAdmin(BasePermission):
    """
    Allows access only to workspace owners
    and admins.
    """

    def has_object_permission(
        self,
        request,
        view,
        obj,
    ):
        return WorkspaceMembership.objects.filter(
            workspace=obj,
            user=request.user,
            role__in=[
                WorkspaceMembership.Role.OWNER,
                WorkspaceMembership.Role.ADMIN,
            ],
        ).exists()

class IsWorkspaceOwner(BasePermission):
    """
    Allows access only to the workspace owner.
    """

    def has_object_permission(
        self,
        request,
        view,
        obj,
    ):
        return WorkspaceMembership.objects.filter(
            workspace=obj,
            user=request.user,
            role=WorkspaceMembership.Role.OWNER,
        ).exists()