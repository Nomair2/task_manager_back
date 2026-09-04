from django.urls import path 
from .views import RegisterView , Loginview
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
]