from django.shortcuts import render
from rest_framework.views import APIView 
from rest_framework import status
from rest_framework.response import Response 
from .serializers import RegisterSerializer  , LoginSerializer , CurrentUserSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView ,
    TokenRefreshView
)
from rest_framework.permissions import IsAuthenticated
from .serializers import LogoutSerializer

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

class LogoutView(APIView):
    def post(self, request):
        serializer = LogoutSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

class CurrentUserView(APIView):
    permission_classes  = [IsAuthenticated]

    def get(self, request ):
        serializer = CurrentUserSerializer(
            request.user
        )

        return Response(
            serializer.data
        )