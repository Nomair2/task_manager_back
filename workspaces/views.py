from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView 
from rest_framework.response import Response
from django.db import transaction
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Workspace , WorkspaceMembership
from .serializers import WorkspaceSerializer , WorkspaceMembershipSerializer
from .permissions import IsWorkspaceMember , IsWorkspaceAdmin , IsWorkspaceOwner

class WorkspaceListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        workspaces = (
            Workspace.objects
            .filter(memberships__user=request.user)
            .distinct()
            .order_by("-created_at")
        )

        serializer = WorkspaceSerializer(
            workspaces,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = WorkspaceSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        with transaction.atomic():
            workspace = serializer.save(
                owner=request.user
            )

            WorkspaceMembership.objects.create(
                workspace=workspace,
                user=request.user,
                role=WorkspaceMembership.Role.OWNER,
            )

        return Response(
            WorkspaceSerializer(workspace).data,
            status=status.HTTP_201_CREATED,
        )


class WorkspaceDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get_workspace(self ,request, workspace_id):
        return get_object_or_404(
            Workspace.objects.filter(
                membership__user =request.user 
            ),
            id= workspace_id
        )

    def get(self , request , workspace_id):
        workspace = self.get_workspace(request ,workspace_id)

        permission = IsWorkspaceMember()

        if not permission.has_object_permission(
            request,
            self ,
            workspace ,
        ):
            return Response(
                {
                    "detail": (
                        "You are not a member of this workspace."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        serialzer = WorkspaceSerializer(workspace )
        return Response(serialzer.data)

    def patch(self , request , workspace_id):
        workspace = self.get_workspace(workspace_id)

        permission = IsWorkspaceAdmin()

        if not permission.has_object_permission(request , self , workspace):
            return Response({
                "detail":(
                    "You do not have permissoin",
                    "to update this workspace."
                )
            },
            status=status.HTTP_403_FORBIDDEN)

        serializer = WorkspaceSerializer(
            workspace ,
            data= request.data , 
            partial= True 
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()
        return Response(
            serializer.data
        )

    def delete(self, request, workspace_id):
        workspace = self.get_workspace(
            workspace_id
        )

        permission = IsWorkspaceOwner()

        if not permission.has_object_permission(
            request,
            self,
            workspace,
        ):
            return Response(
                {
                    "detail": (
                        "Only the workspace owner "
                        "can delete this workspace."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        workspace.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


class WorkspaceMembershipListCreateView(APIView):
    permission_classes = [IsAuthenticated]


    def get(self , request , workspace_id):
        workspace = get_object_or_404(
            Workspace.objects.filter(
                memberships__user = request.user ,

            ) , 
            id = workspace_id,
        )


        memberships = (
            WorkspaceMembership.objects
            .filter(workspace=workspace)
            .select_related("user")
            .order_by("joined_at")
        )

        serializer = WorkspaceMembershipSerializer(
            memberships,
            many=True,
        )
        return Response(serializer.data)

    def post(self , request , workspace_id):

        workspace = get_object_or_404(
            Workspace.objects.filter(
                memberships__user=request.user
            ),
            id=workspace_id,
        )
        permission = IsWorkspaceAdmin()

        if not permission.has_object_permission(
            request , 
            self ,
            workspace
        ):
            return Response(
                {
                    "detail": (
                        "You do not have permission "
                        "to add members."
                        )
                },
                status=status.HTTP_403_FORBIDDEN,
            )



        serializer = WorkspaceMembershipSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        membership = serializer.save(
            workspace=workspace
        )

        return Response(
            WorkspaceMembershipSerializer(
                membership
            ).data,
            status=status.HTTP_201_CREATED,
        )

    