from django.utils import timezone

from services.account import svc_account_create_user, svc_account_create_staff_profile, svc_account_create_user_profile


class AbstractTestSetup:
    def _create_user_account(self):
        self.user_account_data = {
            "phone": "9876543210",
            "password": "password",
            "first_name": "first_name",
            "last_name": "last_name",
            "email": "naveenkumarchava0@gmail.com",
        }

        self.user_account_1 = svc_account_create_user(request_data=self.user_account_data, serialized=False)

    def _create_user_profile(self):
        self.user_profile_data = {
            "phone": self.user_account_data["phone"]
        }

        self.user_profile = svc_account_create_user_profile(request_data=self.admin_profile_data, serialized=False)

    def _create_admin_profile(self):
        self.admin_profile_data = {
            "phone": self.user_account_data["phone"],
            "is_admin": True,
        }

        self.admin_profile = svc_account_create_staff_profile(request_data=self.admin_profile_data, serialized=False)

    @staticmethod
    def _get_epoch_time_for_date(date):
        return int(date.strftime("%s"))

    def _setup_add_event_data(self):
        event_date = timezone.now() + timezone.timedelta(days=10)
        event_date = self._get_epoch_time_for_date(event_date)  # setting event_date as "current day + 10 days"

        booking_open_from = timezone.now() + timezone.timedelta(days=2)
        booking_open_from = self._get_epoch_time_for_date(
            booking_open_from
        )  # setting booking_open_from as "current day + 2 days"

        booking_open_until = timezone.now() + timezone.timedelta(days=3)
        booking_open_until = self._get_epoch_time_for_date(
            booking_open_until
        )  # setting booking_open_from as "current day + 3 days"

        self.event_data_1 = {
            "name": "test event 4",
            "description": "description",
            "event_date": event_date,
            "type": "ONLINE",
            "max_seats": 20,
            "status": "CREATED",
            "location": {"name": "Nellore", "address": "Nellore", "city": "Nellore", "state": "Andhra Pradesh"},
            "booking_windows": [
                {"booking_open_from": booking_open_from, "booking_open_until": booking_open_until},
            ],
            "categories": ["SPORTS"],
            "price_plans": [{"price": 100, "type": "ECONOMY"}, {"price": 200, "type": "PREMIUM"}],
        }
