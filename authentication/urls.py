from django.urls import path 
from .views import ( RegisterView , Loginview , RefreshTokenView , ProtectedTestView)
from rest_framework_simplejwt.views import TokenObtainPairView 

urlpatterns  = [
    path(
        "register/",
        RegisterView.as_view() , 
        name='register',
    ),
    path(
        "login/",
        Loginview.as_view() , 
        name='login',
        ),
    path(
        "token/refresh/",
        RefreshTokenView.as_view() , 
        name='token-refresh',
        ),
        
    path(
        "test/",
        ProtectedTestView.as_view() , 
        name='test',
        ),
]