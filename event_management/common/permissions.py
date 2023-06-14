from rest_framework import status
from rest_framework.permissions import BasePermission
from rest_framework.response import Response


class IsAdminUser(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        try:
            return bool(request.user and request.user.staff_profile.is_admin)
        except AttributeError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)