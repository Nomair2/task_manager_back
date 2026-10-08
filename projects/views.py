from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from workspaces.models import Workspace
from .serializers import ProjectSerializer
from .permissions import CanCreateProject , CanUpdateProject , CanDeleteProject
from .models import Project


class ProjectListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get_workspace(self, request, workspace_id):
        return get_object_or_404(
            Workspace.objects.filter(
                memberships__user=request.user
            ),
            id=workspace_id,
        )

    def get(self, request, workspace_id):
        workspace = self.get_workspace(
            request,
            workspace_id,
        )

        projects = (workspace.projects.select_related(
        "workspace",
        "created_by",
    ).order_by(
            "-created_at"
        ))

        serializer = ProjectSerializer(
            projects,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request, workspace_id):
        workspace = self.get_workspace(
                    request,
                    workspace_id,
                )
        
        permission = CanCreateProject()

        if not permission.has_permission(request , self):
            return Response(
                {'detail':permission.message},
                    status=status.HTTP_403_FORBIDDEN
            )
        

        serializer = ProjectSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        project = serializer.save(
            workspace=workspace,
            created_by=request.user,
        )

        return Response(
            ProjectSerializer(project).data,
            status=status.HTTP_201_CREATED,
        )


class projectDetaillView(APIView):
    permission_classes = [IsAuthenticated]

    def get_workspace(self , request , workspace_id):
        return get_object_or_404(
            Workspace.objects.filter(
                memberships__user = request.user
            ),
            id=workspace_id
        )

    def get_project(
            self , 
            request ,
            workspace_id ,
              project_id
              ):
        return get_object_or_404(
            Project.objects.filter(
                workspace__id = workspace_id ,
                workspace__memberships__user = request.user
                ).select_related(
            "workspace",
            "created_by",
        ) ,
            id = project_id 
            )

    def check_object_permission(self, request, project, permission_class):

        permission = permission_class()

        if not permission.has_object_permission(
            request,
            self,
            project,
        ):
            return Response(
                {"detail": permission.message},
                status=status.HTTP_403_FORBIDDEN,
            )

        return None
    def get(self , request , workspace_id , project_id):
        project = self.get_project(request ,workspace_id , project_id)

        serialzer = ProjectSerializer(project)

        return Response(serialzer.data)


    def patch(self, request, workspace_id, project_id):
        project = self.get_project(
            request,
            workspace_id,
            project_id,
        )
        permission_error = self.check_object_permission(
            request,
            project,
            CanUpdateProject,
        )

        if permission_error:
            return permission_error


        serializer = ProjectSerializer(
            project,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self , request , workspace_id , project_id):
        project = self.get_project(request , workspace_id , project_id)

        permission_error = self.check_object_permission(
            request,
            project,
            CanDeleteProject,
        )

        if permission_error:
            return permission_error

        project.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


