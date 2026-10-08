from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Workspace, WorkspaceMembership


User = get_user_model()


class WorkspaceAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="owner@example.com",
            username="owner",
            password="StrongPassword123!",
        )

        self.client.force_authenticate(
            user=self.user
        )

    def test_create_workspace(self):
        url = reverse(
            "workspace-list-create"
        )

        response = self.client.post(
            url,
            {
                "name": "Acme",
                "slug": "acme",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        workspace = Workspace.objects.get(
            slug="acme"
        )

        self.assertEqual(
            workspace.owner,
            self.user,
        )

        self.assertTrue(
            WorkspaceMembership.objects.filter(
                workspace=workspace,
                user=self.user,
                role=WorkspaceMembership.Role.OWNER,
            ).exists()
        )

    def test_user_only_sees_their_workspaces(self):
        other_user = User.objects.create_user(
            email="other@example.com",
            username="other",
            password="StrongPassword123!",
        )

        other_workspace = Workspace.objects.create(
            name="Other Workspace",
            slug="other-workspace",
            owner=other_user,
        )

        url = reverse(
            "workspace-list-create"
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        workspace_ids = [
            item["id"]
            for item in response.data
        ]

        self.assertNotIn(
            str(other_workspace.id),
            workspace_ids,
        )