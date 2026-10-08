from django.urls import path 
from .views import (
    WorkspaceDetailView,
    WorkspaceListCreateView,
    WorkspaceMembershipListCreateView,
)


urlpatterns = [
    path(
        "",
        WorkspaceListCreateView.as_view(),
        name="workspace-list-create",
    ),

    path(
        "<uuid:workspace_id>/",
        WorkspaceDetailView.as_view(),
        name="workspace-detail",
    ),

    path(
        "<uuid:workspace_id>/members/",
        WorkspaceMembershipListCreateView.as_view(),
        name="workspace-members",
    ),
]