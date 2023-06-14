from functools import wraps

from rest_framework import status
from rest_framework.response import Response


def validate_admin_profile(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        user = request.user

        try:
            if (not user.staff_profile) or (not user.staff_profile.is_admin):
                # if user doesn't have a staff profile and is not admin, raise error
                return Response(
                    {"message": "User doesn't have staff profile or User is not admin"},
                    status=status.HTTP_403_FORBIDDEN,
                )

        except AttributeError as e:
            return Response({"message": "User doesn't have staff profile"}, status=status.HTTP_403_FORBIDDEN)

        return func(self, request, *args, **kwargs)

    return wrapper
