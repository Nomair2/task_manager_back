from django.db import models
from django.conf import settings
import uuid 

# Create your models here.
 

class Workspace(models.Model):
    id = models.UUIDField(
        primary_key=True ,
        default=uuid.uuid4,
        editable=False ,
    )

    name = models.CharField(max_length=250)

    slug = models.SlugField(
        max_length=250 , 
        unique=True 
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL , 
        on_delete=models.PROTECT , 
        related_name='owned_workspaces',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.name





class WorkspaceMembership(models.Model):

    class Role(models.TextChoices):
        OWNER = "OWNER", "Owner"
        ADMIN = "ADMIN", "Admin"
        MEMBER = "MEMBER", "Member"

    id = models.UUIDField(
        primary_key=True , 
        default=uuid.uuid4,
        editable=False 
    )

    workspace = models.ForeignKey(
        Workspace ,
        on_delete=models.CASCADE,
        related_name='memberships'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL , 
        on_delete= models.CASCADE ,
        related_name='workspace_membership',
    )

    role = models.CharField(
        max_length=20 , 
        choices=Role.choices, 
        default=Role.MEMBER
    )

    joined_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['workspace' , 'user'],
                name='unique_workspace_member'
            )
        ]

    def __str__(self):
        return f"{self.user.email} - {self.workspace.name}"