from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from workspaces.models import Workspace, WorkspaceMembership
from .models import Project


User = get_user_model()


class ProjectAPITests(APITestCase):

    def setUp(self):
        self.owner = User.objects.create_user(
            email="owner@example.com",
            username="owner",
            password="StrongPassword123!",
        )

        self.member = User.objects.create_user(
            email="member@example.com",
            username="member",
            password="StrongPassword123!",
        )

        self.workspace = Workspace.objects.create(
            name="Acme",
            slug="acme",
            owner=self.owner,
        )

        WorkspaceMembership.objects.create(
            workspace=self.workspace,
            user=self.owner,
            role=WorkspaceMembership.Role.OWNER,
        )

        WorkspaceMembership.objects.create(
            workspace=self.workspace,
            user=self.member,
            role=WorkspaceMembership.Role.MEMBER,
        )

    def test_member_cannot_create_project(self):
        self.client.force_authenticate(
            user=self.member
        )

        url = reverse(
            "project-list-create",
            kwargs={
                "workspace_id": self.workspace.id,
            },
        )


        response = self.client.post(
            url,
            {
                "name": "Backend",
                "slug": "backend",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.assertFalse(
            Project.objects.filter(
                workspace=self.workspace,
                slug="backend",
            ).exists()
        )

    def test_owner_can_create_project(self):
        self.client.force_authenticate(
            user=self.owner
        )

        url = reverse(
            "project-list-create",
            kwargs={
                "workspace_id": self.workspace.id,
            },
        )

        response = self.client.post(
            url,
            {
                "name": "Backend",
                "slug": "backend",
                "description": "Backend API",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        project = Project.objects.get(
            workspace=self.workspace,
            slug="backend",
        )

        self.assertEqual(
            project.created_by,
            self.owner,
        )


    def test_member_cannot_access_project_from_other_workspace(self):
        other_owner = User.objects.create_user(
            email="other@example.com",
            username="other",
            password="StrongPassword123!",
        )

        other_workspace = Workspace.objects.create(
            name="Other",
            slug="other",
            owner=other_owner,
        )

        WorkspaceMembership.objects.create(
            workspace=other_workspace,
            user=other_owner,
            role=WorkspaceMembership.Role.OWNER,
        )

        project = Project.objects.create(
            workspace=other_workspace,
            name="Secret",
            slug="secret",
            created_by=other_owner,
        )

        self.client.force_authenticate(
            user=self.member
        )

        url = reverse(
            "project-detail",
            kwargs={
                "workspace_id": other_workspace.id,
                "project_id": project.id,
            },
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )