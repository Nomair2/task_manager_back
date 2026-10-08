from django.shortcuts import render , get_object_or_404
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from projects.models import Project
from django.db.models import Q
from .serializers import (
    TaskAssignmentSerializer,
    TaskSerializer,
    TaskStatusSerializer,
    
)

from .workflow import can_transition
from .pagination import TaskPagination
from .permissions import  CanCreateTask , CanUpdateTask , CanDeleteTask , CanAssignTask , CanChangeTaskStatus
from .models import TaskModel

VALID_TASK_STATUSES = {
    choice[0]
    for choice in TaskModel.Status.choices
}

VALID_TASK_PRIORITIES = {
    choice[0]   
    for choice in TaskModel.Priority.choices
}

ALLOWED_TASK_ORDERING_FIELDS = {
    "created_at",
    "updated_at",
    "due_date",
    "title",
}

class TaskListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = TaskPagination

    
    def filter_tasks(self ,queryset , request):
        status_value = request.query_params.get("status")
        priority = request.query_params.get("priority")
        assignee = request.query_params.get("assignee")
        search = request.query_params.get("search")

        if status_value : 
           
            if status_value not in VALID_TASK_STATUSES : 
                raise serializers.ValidationError(
                    {"status": "Invalid task status."}
                )
            
            queryset.filter(
                status = status_value 
            )

        if priority:
            
            if priority not in VALID_TASK_PRIORITIES:
                raise serializers.ValidationError(
                    {"priority": "invalid task priority ."}
                )
            queryset.filter(
                priority = priority
            )

        if assignee: 
            queryset.fitler(
                assignee_id= assignee
            )

        if search : 
            queryset.filter(
                Q(title__icontains = search )
                | Q(description__icontains = search )
            )

        return queryset 


    def order_tasks(self , queryset , request ):
        ordering = request.query_params.get("ordering")

        if not ordering : 
            return queryset.order_by('-created_at')

        descending = ordering.startswith("-")

        field = ordering[1:] if  descending else ordering

        if field not in ALLOWED_TASK_ORDERING_FIELDS:
            raise serializers.ValidationError(
                {'ordering': (
                    f"Invalid ordering field {field}"
                )}
            )

        if descending:
            feild = f"-{field}"

        return queryset.order_by(field)
        

    def get_project(self , request , workspace_id , project_id):
        return get_object_or_404(
            Project.objects.filter(
                workspace__id = workspace_id , 
                workspace__memberships__user = request.user 
            )
             , 
             id = project_id
        )

    def get(self , request , workspace_id , project_id ):
        project = self.get_project(request , workspace_id , project_id  )

        tasks = (
            project.tasks.select_related(
                "project",
                "creator",
                "assignee"
            )
        )

        tasks = self.filter_tasks(tasks , request )

        tasks = self.order_tasks(tasks , request)

        tasks = tasks.order_by("-created_at")

        paginator = self.pagination_class()

        page = paginator.paginate_queryset(
            tasks , request , view=self 
        )
        

        serializer  = TaskSerializer(page , many = True )

        serializer.is_valid(raise_exception=True)

        return paginator.get_paginated_response(
            serializer.data
        )


    def post(self , request , workspace_id , project_id):
        project = self.get_project(request , workspace_id , project_id )

        permission = CanCreateTask()

        if not permission.has_object_permission(request , self ):
            return Response(
                {"detail": permission.massage}, 
                status=403
            )

        task = TaskSerializer(
            data= request.data , 
            context = {
                "workspace":project.workspace
            }
            )
        task.save(
            project = project , 
            creator = request.user 
        )

        return Response(
            TaskSerializer(task).data , 
            status = 201
        )
        

class TaskDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def check_object_permission(
            self , 
            request ,
            task , 
            permission_class 
    ):
        permission = permission_class 

        if not permission.has_object_permission(
            request , self ,task 
        ):
            return Response(
                {
                    'detail':permission.message,
                },
                status=status.HTTP_403_FORBIDDEN
            )
        return None 

    def get_task(
            self , 
            request ,
            workspace_id ,
            project_id , 
            task_id
    ):
        return get_object_or_404(
            TaskModel.objects.filter(
                project__id = project_id , 
                project__workspace__id = workspace_id , 
                project__workspace__memberships__user = request.user 
            ).select_related(
                "creator",
                "project",
                "assignee"
            )
            , id = task_id)

    def get(self , request  , workspace_id , project_id , task_id):

        task = self.get_task(request , workspace_id , project_id , task_id )


        serializer = TaskSerializer(task) 

        return Response(serializer.data)

    def patch(self  ,request , workspace_id , project_id , task_id):

        task = self.get_task(self , request , workspace_id , project_id , task_id)

        permission_error = self.check_object_permission(
            request , task , CanUpdateTask
        )

        if permission_error : 
            return permission_error

        serializer = TaskSerializer(
            task , 
            data = request.data  , 
            partial = True , 
            context = {
                "workspace":task.project.workspace
            }
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(serializer.data)

    def delete(
            self , 
            request , 
            workspace_id ,
            project_id ,
            task_id ,
    ):
        task = self.get_task(request , workspace_id , project_id , task_id)

        permission_error = self.check_object_permission(
            request , task , CanDeleteTask
            )
        
        if permission_error : 
            return permission_error

        task.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    

class TaskAssignmentView(APIView):
    permission_classes = [IsAuthenticated]

    def get_task(
        self,
        request,
        workspace_id,
        project_id,
        task_id,
    ):
        return get_object_or_404(
            TaskModel.objects.filter(
                project__id=project_id,
                project__workspace__id=workspace_id,
                project__workspace__memberships__user=request.user,
            ).select_related(
                "project",
                "creator",
                "assignee",
            ),
            id=task_id,
        )

    def post(
        self,
        request,
        workspace_id,
        project_id,
        task_id,
    ):
        task = self.get_task(
            request,
            workspace_id,
            project_id,
            task_id,
        )
        permission_error = self.check_object_permission(
           request,
            task,
            CanAssignTask,
            )

        if permission_error:
            return permission_error

        serializer = TaskAssignmentSerializer(
            data=request.data,
            context={
                "workspace": task.project.workspace,
            },
        )

        serializer.is_valid(
            raise_exception=True
        )

        task.assignee = serializer.validated_data.get(
            "assignee"
        )

        task.save(
            update_fields=[
                "assignee",
                "updated_at",
            ]
        )

        return Response(
            TaskSerializer(task).data
        )


class TaskStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get_task(
        self,
        request,
        workspace_id,
        project_id,
        task_id,
    ):
        return get_object_or_404(
            TaskModel.objects.filter(
                project__id=project_id,
                project__workspace__id=workspace_id,
                project__workspace__memberships__user=request.user,
            ).select_related(
                "project",
                "creator",
                "assignee",
            ),
            id=task_id,
        )

    def post(
        self,
        request,
        workspace_id,
        project_id,
        task_id,
    ):
        task = self.get_task(
            request,
            workspace_id,
            project_id,
            task_id,
        )

        permission_error = self.check_object_permission(
            request,
            task,
            CanChangeTaskStatus,
            )

        if permission_error:
            return permission_error

        serializer = TaskStatusSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        new_status = serializer.validated_data["status"]

        if task.status == new_status:
            return Response(
                {
                    "detail": "Task is already in this status."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not can_transition(
            task.status,
            new_status,
        ):
            return Response(
                {
                    "detail": (
                        f"Cannot transition task from "
                        f"{task.status} to {new_status}."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        task.status = new_status

        task.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        return Response(
            TaskSerializer(task).data,
            status=status.HTTP_200_OK,
        )


