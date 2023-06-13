import uuid
from typing import Union
import phonenumbers

from rest_framework.request import Request
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, get_user_model

from account.models import UserProfile, StaffProfile
from account.api.serializers import BaseUserSerializer, StaffProfileSerializer

User = get_user_model()


def _validate_phone_number(phone_number: str):
    try:
        phone_number = phone_number.strip()

        if len(phone_number) == 10 and (not phone_number.startswith("+")):
            # the input phone number doesn't have the country code.
            # adding +91 to the phone number
            phone_number = "+" + str(91) + phone_number
        elif len(phone_number) == 12 and (not phone_number.startswith("+")):
            phone_number = "+" + phone_number

        phone_number = phonenumbers.parse(phone_number)

        is_valid_number = phonenumbers.is_valid_number(phone_number)

        if not is_valid_number:
            raise ValueError("Invalid phone number")

        phone_number = phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.E164)

        return phone_number
    except phonenumbers.phonenumberutil.NumberParseException as e:
        raise ValueError(f"{str(e)}")


def _get_or_create_user_token(user: User) -> str:
    token = Token.objects.get_or_create(user=user)

    return token[0].key


def svc_account_create_user(request_data: dict, serialized: bool = True) -> Union[User, dict]:
    if "phone" not in request_data:
        raise ValueError("phone missing in the request data")
    if "password" not in request_data:
        raise ValueError("password missing in the request data")
    if "first_name" not in request_data:
        raise ValueError("first_name missing in the request data")

    phone = request_data["phone"]
    password = request_data["password"]
    first_name = request_data["first_name"]
    last_name = request_data.get("last_name", "")
    email = request_data.get("email", None)

    phone = _validate_phone_number(phone)

    # create user
    user = User.objects.create_user(
        phone=phone, password=password, first_name=first_name, last_name=last_name, email=email
    )
    user.save()

    if serialized:
        return BaseUserSerializer(user, many=False).data
    return user


def svc_account_create_user_profile(request_data: dict, serialized: bool = True) -> Union[UserProfile, dict]:
    if "phone" not in request_data:
        raise ValueError("phone missing in the request data")

    phone = request_data["phone"]

    user = User.objects.get(phone=phone)
    user_profile = UserProfile.create(user=user)

    if serialized:
        return BaseUserSerializer(user_profile.user, many=False).data
    return user_profile


def svc_account_create_staff_profile(request_data: dict, serialized: bool = True) -> Union[UserProfile, dict]:
    if "phone" not in request_data:
        raise ValueError("phone missing in the request data")

    phone = request_data["phone"]
    is_admin = request_data.get("is_admin", False)

    user = User.objects.get(phone=phone)

    staff_profile = StaffProfile.create(user=user)
    staff_profile.is_admin = is_admin
    staff_profile.save()

    if serialized:
        return StaffProfileSerializer(staff_profile, many=False).data
    return staff_profile


def svc_account_login_user(request: Request) -> None:
    request_data = request.data

    if "phone" not in request_data:
        raise ValueError("phone missing in the request data")
    if "password" not in request_data:
        raise ValueError("Password missing in the request data")

    phone = request_data["phone"]
    password = request_data["password"]

    user = authenticate(phone=phone, password=password)

    token = _get_or_create_user_token(user)

    if not user:
        raise ValueError("Invalid phone or password")

    login(request, user)

    return token
