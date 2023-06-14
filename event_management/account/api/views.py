from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response

from services.account import (
    svc_account_create_user,
    svc_account_create_user_profile,
    svc_account_create_staff_profile,
    svc_account_login_user,
)

User = get_user_model()

class UserSignupView(generics.GenericAPIView): # create user account
    def post(self, request, **kwargs):
        try:
            return Response(svc_account_create_user(request_data=request.data), status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({"message": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({"message": "Invalid email address"}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.GenericAPIView): # create user profile
    def post(self, request, **kwargs):
        try:
            return Response(svc_account_create_user_profile(request_data=request.data), status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({"message": "User Profile already exists"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist as e:
            return Response({"message": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)


class StaffProfileView(generics.GenericAPIView): # create staff profile
    def post(self, request, **kwargs):
        try:
            return Response(svc_account_create_staff_profile(request_data=request.data), status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({"message": "Staff Profile already exists"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist as e:
            return Response({"message": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(generics.GenericAPIView): # login user -> user, staff
    def post(self, request, **kwargs):
        try:
            token = svc_account_login_user(request)
            return Response({"token": token}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# class UserLogoutView(generics.GenericAPIView):

#     def post(self, request, **kwargs):
#         svc_account_logout_user(request.user)
#         return Response({"message": "User logged out successfully."}, status=status.HTTP_204_NO_CONTENT)
