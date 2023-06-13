from rest_framework import serializers
from django.utils import timezone

from event.models import Event, Category, Location, Ticket, PricePlan, BookingWindow
from common.constants import EventType, EventStatusType, EventPriceType


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ("name", "address", "city", "state")


class PricePlanSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = PricePlan
        fields = (
            "price",
            "type",
        )

    def get_type(self, obj: PricePlan) -> str:
        type = obj.get_type()
        return EventPriceType.get_string_for_obj(type)


class BookingWindowSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingWindow
        fields = (
            "booking_open_from",
            "booking_open_until",
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name",)


class EventSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()

    price_plan = serializers.SerializerMethodField()
    booking_windows = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = (
            "external_id",
            "created",
            "modified",
            "name",
            "description",
            "event_date",
            "type",
            "max_seats",
            "status",
            "location",
            "price_plan",
            "booking_windows",
            "categories",
        )

    def get_type(self, obj: Event) -> str:
        type = obj.get_event_type()
        return EventType.get_string_for_obj(type)

    def get_status(self, obj: Event) -> str:
        status = obj.get_event_status()
        return EventStatusType.get_string_for_obj(status)

    def get_location(self, obj: Event) -> dict:
        return LocationSerializer(obj.location, many=False).data

    def get_price_plan(self, obj: Event) -> dict:
        return PricePlanSerializer(obj.price_plans, many=True).data

    def get_booking_windows(self, obj: Event) -> dict:
        return BookingWindowSerializer(obj.booking_windows, many=True).data

    def get_categories(self, obj: Event) -> dict:
        return CategorySerializer(obj.categories, many=True).data


class EventUserSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    available_seats = serializers.SerializerMethodField()

    price_plan = serializers.SerializerMethodField()
    booking_open = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = (
            "external_id",
            "name",
            "description",
            "event_date",
            "type",
            "available_seats",
            "status",
            "location",
            "price_plan",
            "booking_open",
            "categories",
        )

    def get_type(self, obj: Event) -> str:
        type = obj.get_event_type()
        return EventType.get_string_for_obj(type)

    def get_status(self, obj: Event) -> str:
        status = obj.get_event_status()
        return EventStatusType.get_string_for_obj(status)

    def get_location(self, obj: Event) -> dict:
        return LocationSerializer(obj.location, many=False).data

    def get_price_plan(self, obj: Event) -> dict:
        return PricePlanSerializer(obj.price_plans, many=True).data

    def get_booking_open(self, obj: Event) -> dict:
        booking_windows = BookingWindow.objects.filter(event=obj)

        for booking_window in booking_windows:
            if booking_window.booking_open_from >= timezone.now() > booking_window.booking_open_until:
                return True
        return False

    def get_categories(self, obj: Event) -> dict:
        return CategorySerializer(obj.categories, many=True).data

    def get_available_seats(self, obj: Event) -> int:
        return obj.get_available_seats()


class TicketSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    event_date = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = (
            "external_id",
            "created",
            "name",
            "description",
            "event_date",
            "type",
            "status",
            "location",
            "categories",
        )

    def get_name(self, obj: Ticket) -> str:
        return obj.event.get_name()

    def get_description(self, obj: Ticket) -> str:
        return obj.event.get_description()

    def get_event_date(self, obj: Ticket) -> str:
        return obj.event.get_event_date()

    def get_name(self, obj: Ticket) -> str:
        return obj.event.get_name()

    def get_name(self, obj: Ticket) -> str:
        return obj.event.get_name()

    def get_type(self, obj: Ticket) -> str:
        type = obj.event.get_event_type()
        return EventType.get_string_for_obj(type)

    def get_status(self, obj: Ticket) -> str:
        status = obj.event.get_event_status()
        return EventStatusType.get_string_for_obj(status)

    def get_location(self, obj: Ticket) -> dict:
        return LocationSerializer(obj.event.location, many=False).data

    def get_categories(self, obj: Ticket) -> dict:
        return CategorySerializer(obj.event.categories, many=True).data
