from django.urls import path

from .views import (
    TaskAssignmentView,
    TaskDetailView,
    TaskListCreateView,
    TaskStatusView,
)

urlpatterns = [
    path(
        "",
        TaskListCreateView.as_view(),
        name="task-list-create",
    ),
    path(
            "<uuid:task_id>/",
            TaskDetailView.as_view(),
            name="task-detail",
        ),
    path(
        "<uuid:task_id>/assign/",
        TaskAssignmentView.as_view(),
        name="task-assign",
    ),
    path(
        "<uuid:task_id>/status/",
        TaskStatusView.as_view(),
        name="task-status",
    ),
]