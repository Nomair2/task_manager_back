from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser 


# Create your models here.


class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True , 
        default=uuid.uuid4,
        editable=False 
    )

    email= models.EmailField(unique=True )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =['username']

    def __str__(self):
        return self.email