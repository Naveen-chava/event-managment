import json

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from common.abstract_test_setups import AbstractTestSetup


class UserSignupAPI(APITestCase):
    def setUp(self):
        self.url = reverse("account:handler-user-signup")

    def test_create_user_account(self):
        request_data = {
            "phone": "9876543210",
            "password": "password",
            "first_name": "first_name",
            "last_name": "last_name",
            "email": "naveenkumarchava0@gmail.com",
        }

        response = self.client.post(self.url, data=json.dumps(request_data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], request_data["email"])

    def test_create_user_account_missing_fields(self):
        request_data = {
            # "phone": "9876543210", # removed the "phone" to cause an error
            "password": "password",
            "first_name": "first_name",
            "last_name": "last_name",
            "email": "naveenkumarchava0@gmail.com",
        }

        response = self.client.post(self.url, data=json.dumps(request_data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "phone missing in the request data")

        request_data = {
            "phone": "9876543210",
            # "password": "password",  # removed the "password" to cause an error
            "first_name": "first_name",
            "last_name": "last_name",
            "email": "naveenkumarchava0@gmail.com",
        }

        response = self.client.post(self.url, data=json.dumps(request_data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "password missing in the request data")

        request_data = {
            "phone": "9876543210",
            "password": "password",
            # "first_name": "first_name", # removed the "password" to cause an error
            "last_name": "last_name",
            "email": "naveenkumarchava0@gmail.com",
        }

        response = self.client.post(self.url, data=json.dumps(request_data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "first_name missing in the request data")

    def test_create_user_account_invalid_phone_number(self):
        request_data = {
            "phone": "1111111111",  # invalid phone number
            "password": "password",
            "first_name": "first_name",
            "last_name": "last_name",
            "email": "naveenkumarchava0@gmail.com",
        }

        response = self.client.post(self.url, data=json.dumps(request_data), content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Invalid phone number")

    def test_create_user_account_invalid_email(self):
        request_data = {
            "phone": "9876543210",
            "password": "password",
            "first_name": "first_name",
            "last_name": "last_name",
            "email": "This is an invalid email",  # invalid email id
        }

        response = self.client.post(self.url, data=json.dumps(request_data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Invalid email address")

    def test_create_user_account_duplicate_user(self):
        request_data = {
            "phone": "9876543210",
            "password": "password",
            "first_name": "first_name",
            "last_name": "last_name",
            "email": "naveenkumarchava0@gmail.com",
        }

        # creating the user
        response = self.client.post(self.url, data=json.dumps(request_data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], request_data["email"])

        # creating the user with same data again
        response = self.client.post(self.url, data=json.dumps(request_data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "User already exists")


class UserProfileAPI(APITestCase, AbstractTestSetup):
    def setUp(self):
        self._create_user_account()
        self.url = reverse("account:handler-user-profile")

    def test_create_user_profile(self):
        request_data = {
            "phone": self.user_account_data["phone"],
        }

        response = self.client.post(self.url, data=json.dumps(request_data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user_account_data["email"])

    def test_create_user_profile_missing_phone(self):
        request_data = {
            # "phone": self.user_account_data["phone"],  # removed the "phone" to cause an error
        }

        response = self.client.post(self.url, data=json.dumps(request_data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "phone missing in the request data")

    def test_create_user_profile_duplicate_profile(self):
        request_data = {
            "phone": self.user_account_data["phone"],
        }

        # creating user profile
        response = self.client.post(self.url, data=json.dumps(request_data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user_account_data["email"])

        # creating the user with same data again
        response = self.client.post(self.url, data=json.dumps(request_data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "User Profile already exists")

    def test_create_user_profile_user_account_does_not_exist(self):
        request_data = {
            "phone": "8142823320",  # a user with this phone number does not exist
        }

        response = self.client.post(self.url, data=json.dumps(request_data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "User does not exist")


class StaffProfileAPI(APITestCase, AbstractTestSetup):
    def setUp(self):
        self._create_user_account()
        self.url = reverse("account:handler-staff-profile")

    def test_create_staff_profile(self):
        request_data = {
            "phone": self.user_account_data["phone"],
        }

        response = self.client.post(self.url, data=json.dumps(request_data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["staff_profile"]["email"], self.user_account_data["email"])

    def test_create_staff_profile_as_admin(self):
        request_data = {"phone": self.user_account_data["phone"], "is_admin": True}

        response = self.client.post(self.url, data=json.dumps(request_data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["staff_profile"]["email"], self.user_account_data["email"])

    def test_create_staff_profile_missing_phone(self):
        request_data = {
            # "phone": self.user_account_data["phone"],  # removed the "phone" to cause an error
        }

        response = self.client.post(self.url, data=json.dumps(request_data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "phone missing in the request data")

    def test_create_staff_profile_duplicate_profile(self):
        request_data = {
            "phone": self.user_account_data["phone"],
        }

        # creating user profile
        response = self.client.post(self.url, data=json.dumps(request_data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["staff_profile"]["email"], self.user_account_data["email"])

        # creating the user with same data again
        response = self.client.post(self.url, data=json.dumps(request_data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Staff Profile already exists")

    def test_create_staff_profile_user_account_does_not_exist(self):
        request_data = {
            "phone": "8142823320",  # a user with this phone number does not exist
        }

        response = self.client.post(self.url, data=json.dumps(request_data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "User does not exist")


class UserLoginAPI(APITestCase, AbstractTestSetup):
    def setUp(self):
        self._create_user_account()
        self.url = reverse("account:handler-user-login")

    def test_create_user_login(self):
        request_data = {"phone": self.user_account_data["phone"], "password": self.user_account_data["password"]}

        response = self.client.post(self.url, data=json.dumps(request_data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user_login_missing_data(self):
        request_data = {
            # "phone": self.user_account_data["phone"],  # removed the "phone" to cause an error
            "password": self.user_account_data["password"]
        }

        response = self.client.post(self.url, data=json.dumps(request_data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "phone missing in the request data")

        request_data = {
            "phone": self.user_account_data["phone"],
            # "password": self.user_account_data["password"]  # removed the "password" to cause an error
        }

        response = self.client.post(self.url, data=json.dumps(request_data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Password missing in the request data")

    def test_create_user_login_invalid_phone(self):
        request_data = {"phone": "1111111111", "password": self.user_account_data["password"]}

        response = self.client.post(self.url, data=json.dumps(request_data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Invalid phone or password")
