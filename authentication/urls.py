from django.urls import path 
from .views import ( RegisterView , Loginview , RefreshTokenView , ProtectedTestView , LogoutView , CurrentUserView)
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
    path(
    "logout/",
    LogoutView.as_view(),
    name="logout",
    ),
    path(
    "me/",
    CurrentUserView.as_view(),
    name="current-user",
),

]