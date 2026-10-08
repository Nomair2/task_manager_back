from django.urls import path
from .views import ProjectListCreateView , projectDetaillView

urlpatterns = [
    path(
        "",
        ProjectListCreateView.as_view(),
        name="project-list-create"
    ),
    path(
        "<uuid:project_id>/",
        projectDetaillView.as_view(),
        name="project-detail"
    ),
]