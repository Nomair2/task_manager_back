from django.shortcuts import render
from rest_framework.views import APIView 
from rest_framework import status
from rest_framework.response import Response 
from .serializers import RegisterSerializer 

# Create your views here.


class RegisterView(APIView):

    def post(self , request):
        serializer = RegisterSerializer(
            data =  request.data
        )

        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response(
            {
                'id':str(user.id),
                'email':user.email , 
                'username':user.username
            },
            status=status.HTTP_201_CREATED
        )