from rest_framework.response import Response
from rest_framework import status

def check_object_permission(
    self,
    request,
    task,
    permission_class,
):
    permission = permission_class()

    if not permission.has_object_permission(
        request,
        self,
        task,
    ):
        return Response(
            {"detail": permission.message},
            status=status.HTTP_403_FORBIDDEN,
        )

    return None