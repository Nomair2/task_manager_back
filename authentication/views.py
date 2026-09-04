from django.shortcuts import render
from rest_framework.views import APIView 
from rest_framework import status
from rest_framework.response import Response 
from .serializers import RegisterSerializer  , LoginSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView ,
    TokenRefreshView
)
from rest_framework.permissions import IsAuthenticated

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


class Loginview(TokenObtainPairView):
    serializer_class  = LoginSerializer

class RefreshTokenView(TokenRefreshView):
    pass

class ProtectedTestView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self , request):
        return Response(
            {
                'message':"You are protected ", 
                'user_id':str(request.user.id),
                'email':request.user.email ,
            }
        )