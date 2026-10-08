from django.db import models

# Create your models here.
import uuid

from django.conf import settings
from django.db import models


class TaskModel(models.Model):

    class Status(models.TextChoices):
        TODO = "TODO", "To Do"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        REVIEW = "REVIEW", "Review"
        DONE = "DONE", "Done"

    class Priority(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"
        URGENT = "URGENT", "Urgent"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="tasks",
    )

    title = models.CharField(
        max_length=255,
    )

    description = models.TextField(
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.TODO,
    )

    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_tasks",
    )

    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tasks",
    )

    due_date = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        indexes = [
            models.Index(
                fields=["project"],
                name="task_project_idx",
            ),
            models.Index(
                fields=["assignee"],
                name="task_assignee_idx",
            ),
            models.Index(
                fields=["status"],
                name="task_status_idx",
            ),
            models.Index(
                fields=["due_date"],
                name="task_due_date_idx",
            ),
        ]

    def __str__(self):
        return self.title