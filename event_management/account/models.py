from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email

from phonenumber_field.modelfields import PhoneNumberField

from common.abstract_models import AbstractDateTimeStamp, AbstractExternalID


class CustomUserManager(BaseUserManager):
    def create_user(
        self,
        phone: str,
        password: str,
        first_name: str,
        last_name: str = "",
        email: str = "",
    ) -> "User":
        """
        Creates and saves a User with the given phone, password, first_name.
        """
        if not phone:
            raise ValueError("Users must have a phone number ")

        user = self.model(phone=phone, email=email, first_name=first_name, last_name=last_name)

        user.set_password(password)

        if email:
            user.set_email(email)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        phone: str,
        password: str,
        first_name: str,
        last_name: str = "",
        email: str = "",
    ):  # pragma: no cover
        """
        Creates and saves a superuser with the given phone, password, first_name.
        """
        user = self.create_user(
            phone=phone, password=password, first_name=first_name, last_name=last_name, email=email
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser, AbstractDateTimeStamp, AbstractExternalID):
    username = None
    email_verified = models.BooleanField(default=False)
    is_suspended = models.BooleanField(default=False)

    phone = PhoneNumberField(null=False, blank=False, unique=True)
    phone_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["first_name"]

    objects = CustomUserManager()

    def __str__(self) -> str:  # pragma: no cover
        return str(self.phone)

    class Meta:
        db_table = "user"

    def set_email(self, email: str, save=False):
        validate_email(email)
        self.email = email
        if save:
            self.save()
        return self

    def get_profile_name(self) -> str:
        return self.first_name + self.last_name if self.last_name else self.first_name


class UserProfile(AbstractDateTimeStamp, AbstractExternalID):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field="external_id", related_name="user_profile"
    )

    def __str__(self) -> str:
        return f"{self.user.first_name} - {self.user.phone}"

    @classmethod
    def create(cls, user: User) -> "UserProfile":
        user_profile = UserProfile(user=user)
        user_profile.save()
        return user_profile


class StaffProfile(AbstractDateTimeStamp, AbstractExternalID):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field="external_id", related_name="staff_profile"
    )
    is_admin = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.user.first_name} - {self.user.phone}"

    @classmethod
    def create(cls, user: User) -> "StaffProfile":
        staff_profile = StaffProfile(user=user)
        staff_profile.save()
        return staff_profile
