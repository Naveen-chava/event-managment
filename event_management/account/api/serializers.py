from rest_framework import serializers

from account.models import User, UserProfile, StaffProfile


class BaseUserSerializer(serializers.ModelSerializer):
    external_id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "phone",
            "phone_verified",
            "email",
            "email_verified",
            "is_active",
            "is_suspended",
            "created",
            "modified",
            "external_id",
        )

    def get_external_id(self, obj: User) -> str:
        return obj.get_external_id(_str=True)


class StaffProfileSerializer(serializers.ModelSerializer):
    staff_profile = serializers.SerializerMethodField()
    is_staff = serializers.SerializerMethodField()

    class Meta:
        model = StaffProfile
        fields = (
            "staff_profile",
            "is_staff",
            "is_admin",
        )

    def get_is_staff(self, obj: UserProfile) -> bool:
        return obj.user.is_staff

    def get_staff_profile(self, obj: UserProfile) -> dict:
        return BaseUserSerializer(obj.user, many=False).data
