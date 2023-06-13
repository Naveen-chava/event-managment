from django.db import models

from account.models import User
from common.constants import Length, EventType, EventStatusType, EventCategoryType, EventPriceType
from common.abstract_models import AbstractDateTimeStamp, AbstractExternalID


class Location(AbstractDateTimeStamp):
    name = models.CharField(max_length=Length.LOCATION_NAME)
    address = models.CharField(max_length=Length.ADDRESS)
    city = models.CharField(max_length=Length.CITY)
    state = models.CharField(max_length=Length.STATE)

    def __str__(self) -> str:
        return self.name

    def set_name(self, name, save: bool = False) -> "Location":
        self.name = name
        if save:
            self.save()
        return self

    def set_address(self, address, save: bool = False) -> "Location":
        self.address = address
        if save:
            self.save()
        return self

    def set_city(self, city, save: bool = False) -> "Location":
        self.city = city
        if save:
            self.save()
        return self

    def set_state(self, state, save: bool = False) -> "Location":
        self.state = state
        if save:
            self.save()
        return self


class Event(AbstractDateTimeStamp, AbstractExternalID):
    name = models.CharField(max_length=Length.EVENT_NAME)
    description = models.TextField()
    event_date = models.DateTimeField()
    type = models.PositiveIntegerField(choices=EventType.get_choices(), default=EventType.OFFLINE)

    max_seats = models.PositiveIntegerField(default=0)

    status = models.PositiveIntegerField(choices=EventStatusType.get_choices(), default=EventStatusType.CREATED)

    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name="events")

    def __str__(self) -> str:
        return self.name

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str, save: bool = False) -> "Event":
        self.name = name
        if save:
            self.save()
        return self

    def get_description(self) -> str:
        return self.description

    def set_description(self, description: str, save: bool = False) -> "Event":
        self.description = description
        if save:
            self.save()
        return self

    def set_event_date(self, event_date, save: bool = False) -> "Event":
        self.event_date = event_date
        if save:
            self.save()
        return self

    def get_event_date(self):
        return self.event_date

    def set_type(self, type: str, save: bool = False) -> "Event":
        type = EventType.get_obj_for_string(type)
        self.type = type
        if save:
            self.save()
        return self

    def set_available_seats(self, max_seats: int, save: bool = False) -> "Event":
        self.max_seats = max_seats
        if save:
            self.save()
        return self

    def set_status(self, status: str, save: bool = False) -> "Event":
        status = EventStatusType.get_obj_for_string(status)
        self.status = status
        if save:
            self.save()
        return self

    def get_available_seats(self) -> int:
        return self.max_seats - self.tickets.count()
        # 'tickets' is a reverse relation. 'tickets' allows us to access all the Ticket instances related to a particular Event instance

    def get_event_type(self) -> int:
        return self.type

    def get_event_status(self) -> int:
        return self.status

    def set_location(self, location: Location, save: bool = False) -> "Event":
        self.location = location
        if save:
            self.save()
        return self

    def get_location(self) -> "Location":
        return self.location

    @classmethod
    def create(cls, name, description, event_date, type, max_seats, status):
        event = cls(
            name=name, description=description, event_date=event_date, type=type, max_seats=max_seats, status=status
        )

        event.save()
        return event


class PricePlan(AbstractDateTimeStamp):
    price = models.FloatField()
    type = models.PositiveIntegerField(choices=EventPriceType.get_choices(), default=EventPriceType.SAME)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="price_plans")

    def __str__(self) -> str:
        return f"{self.type} - {self.price}"

    def get_type(self) -> int:
        return self.type


class BookingWindow(AbstractDateTimeStamp):
    booking_open_from = models.DateTimeField()
    booking_open_until = models.DateTimeField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="booking_windows")

    def __str__(self) -> str:
        return f"{self.booking_open_from} - {self.booking_open_until}"

    @classmethod
    def create(cls, booking_open_from, booking_open_until) -> "BookingWindow":
        booking_window = cls(booking_open_from, booking_open_until)

        booking_window.save()
        return booking_window


class Category(AbstractDateTimeStamp):
    name = models.PositiveIntegerField(choices=EventCategoryType.get_choices(), default=EventCategoryType.OTHERS)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="categories")

    def __str__(self) -> str:
        return self.name


class Ticket(AbstractDateTimeStamp, AbstractExternalID):
    event = models.ForeignKey(Event, null=True, on_delete=models.SET_NULL, related_name="tickets")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Ticket {self.external_id} - {self.event.name}"


"""
Admin:
- Can create event
- Can update event
- Can delete event. 
- Can update all the fields in Event model
- Can get list of booking windows of an event
- Can get list of categories of an event


User: 
- Book tickets
- View booked tickets
- view all events sorted by event chronologically
- Can get the available seats
- Can view all the events
- Can get details of a particular event based on uuid
"""
