from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView 
from rest_framework.response import Response
from django.db import transaction
from rest_framework import status

from .models import Workspace , WorkspaceMembership
from .serializers import WorkspaceSerializer



class WorkspaceListCreateView(APIView):
    permission_classes = [IsAuthenticated]


    def get(self , request):
        pass 

    def post(self , request):

        serializer = WorkspaceSerializer(
            data = request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        with transaction.atomic():
            workspace = serializer.save(
                owner= request.user , 
            )

            WorkspaceMembership.objects.create(
                user = request.user , 
                role = WorkspaceMembership.Role.OWNER ,
                workspace = workspace
            )

        return Response(
            WorkspaceSerializer(workspace).data ,
            status=status.HTTP_201_CREATED
        )