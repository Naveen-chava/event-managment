import json

from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase

from common.abstract_test_setups import AbstractTestSetup
from common.constants import EventStatusType


class EventAdminAPI(APITestCase, AbstractTestSetup):
    def setUp(self):
        self._create_user_account()
        self._create_admin_profile()
        self._setup_add_event_data()
        self.user = self.admin_profile.user
        self.url = reverse("event:handler-event-admin-list-view")

    def test_create_event(self):
        self.client.force_authenticate(user=self.user)

        request_data = self.event_data_1

        response = self.client.post(self.url, data=json.dumps(request_data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.event_data_1["name"])
        self.assertEqual(response.data["status"], self.event_data_1["status"])
        self.assertEqual(response.data["max_seats"], self.event_data_1["max_seats"])
        self.assertEqual(response.data["location"]["city"], self.event_data_1["location"]["city"])
        self.assertEqual(response.data["location"]["address"], self.event_data_1["location"]["address"])

    def test_create_event_missing_booking_open_from(self):
        self.client.force_authenticate(user=self.user)

        request_data = self.event_data_1

        del request_data["booking_windows"][0]["booking_open_from"]

        response = self.client.post(self.url, data=json.dumps(request_data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "booking_open_from missing")

    def test_create_event_missing_booking_open_from_greater_than_event_date(self):
        self.client.force_authenticate(user=self.user)

        request_data = self.event_data_1

        booking_open_from = timezone.now() + timezone.timedelta(days=20)
        booking_open_from = self._get_epoch_time_for_date(
            booking_open_from
        )  # setting booking_open_from as "current day + 20 days"

        request_data["booking_windows"][0]["booking_open_from"] = booking_open_from

        response = self.client.post(self.url, data=json.dumps(request_data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "booking_open_from cannot be greater than event_date")

    def test_create_event_without_booking_open_until(self):
        self.client.force_authenticate(user=self.user)

        request_data = self.event_data_1

        del request_data["booking_windows"][0]["booking_open_until"]

        response = self.client.post(self.url, data=json.dumps(request_data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["event_date"], response.data["booking_windows"][0]["booking_open_until"])

    def test_create_event_invalid_max_seats(self):
        self.client.force_authenticate(user=self.user)

        request_data = self.event_data_1

        request_data["max_seats"] = -1

        response = self.client.post(self.url, data=json.dumps(request_data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "CHECK constraint failed: event_event")

    def test_create_event_invalid_status(self):
        self.client.force_authenticate(user=self.user)

        request_data = self.event_data_1

        request_data["status"] = "Some Invalid Status"

        response = self.client.post(self.url, data=json.dumps(request_data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Invalid key 'Some Invalid Status'")

    def test_create_event_user_deosnt_have_staff_profile(self):
        self._create_user_profile()
        user = self.user_profile
        self.client.force_authenticate(user=user)

        request_data = self.event_data_1

        response = self.client.post(self.url, data=json.dumps(request_data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["message"], "User doesn't have staff profile")

    def test_create_event_user_is_not_an_admin(self):
        user = self.user
        user.staff_profile.is_admin = False
        user.staff_profile.save()

        self.client.force_authenticate(user=user)

        request_data = self.event_data_1

        response = self.client.post(self.url, data=json.dumps(request_data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["message"], "User doesn't have staff profile or User is not admin")
