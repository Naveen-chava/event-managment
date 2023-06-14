import uuid
from typing import Union, List
from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction

from common.constants import EventCategoryType, EventType, EventStatusType, EventPriceType
from event.models import Event, BookingWindow, Location, Category, PricePlan, Ticket
from event.api.serializers import EventSerializer, EventUserSerializer, TicketSerializer


User = get_user_model()


def _get_datetime_for_epoch_time(time):
    return datetime.fromtimestamp(time)


def _validate_create_event_request_data(request_data: dict):
    if "name" not in request_data:
        raise ValueError("name is missing in request_data")

    if "description" not in request_data:
        raise ValueError("description is missing in request_data")

    if "event_date" not in request_data:
        raise ValueError("event_date is missing in request_data")

    if "type" not in request_data:
        raise ValueError("type is missing in request_data")

    if "max_seats" not in request_data:
        raise ValueError("max_seats is missing in request_data")

    if "status" not in request_data:
        raise ValueError("status is missing in request_data")

    if "location" in request_data:
        if "name" not in request_data["location"]:
            raise ValueError("name is missing in location")

        if "address" not in request_data["location"]:
            raise ValueError("address is missing in location")

        if "city" not in request_data["location"]:
            raise ValueError("city is missing in location")

        if "state" not in request_data["location"]:
            raise ValueError("state is missing in location")


def _get_booking_open_from_and_booking_open_until(booking_window: dict, event: Event):
    if "booking_open_from" not in booking_window:
        raise ValueError(f"booking_open_from missing")

    booking_open_from = booking_window["booking_open_from"]
    booking_open_until = booking_window.get("booking_open_until")

    booking_open_from = _get_datetime_for_epoch_time(booking_open_from)

    event_date = event.get_event_date()
    if isinstance(event_date, int):
        event_date = _get_datetime_for_epoch_time(event_date)

    if booking_open_from > event_date:  # event.event_date:
        raise ValueError("booking_open_from cannot be greater than event_date")

    if not booking_open_until:
        # if to_date is not available, use event's date as to_date
        booking_open_until = event.event_date
    else:
        booking_open_until = _get_datetime_for_epoch_time(booking_open_until)

    return booking_open_from, booking_open_until


def _create_booking_windows(booking_windows: list, event: Event) -> None:
    for booking_window in booking_windows:
        booking_open_from, booking_open_until = _get_booking_open_from_and_booking_open_until(booking_window, event)

        booking_window = BookingWindow.objects.create(
            booking_open_from=booking_open_from, booking_open_until=booking_open_until, event=event
        )


def _create_categories(categories: list, event: Event) -> None:
    for category in categories:
        category = EventCategoryType.get_obj_for_string(category)
        category = Category.objects.create(name=category, event=event)


def _create_location(location: dict) -> "Location":
    name = location["name"]
    address = location["address"]
    city = location["city"]
    state = location["state"]

    location = Location.objects.create(name=name, address=address, city=city, state=state)

    return location


def _create_price_plans(price_plans, event) -> "PricePlan":
    for price_plan in price_plans:
        if "price" not in price_plan:
            raise ValueError("price missing in price_plan")
        if "type" not in price_plan:
            raise ValueError("type missing in price_plan")

        price = price_plan["price"]
        type = EventPriceType.get_obj_for_string(price_plan["type"])
        price_plan = PricePlan.objects.create(price=price, type=type, event=event)


def svc_event_create_event(request_data: dict, serialized: bool = True) -> Union["Event", dict]:
    with transaction.atomic():
        _validate_create_event_request_data(request_data)

        name = request_data["name"]
        description = request_data["description"]
        event_date = request_data["event_date"]
        type = request_data["type"]
        max_seats = request_data["max_seats"]
        status = request_data["status"]

        categories = request_data.get("categories", [])

        event_date = _get_datetime_for_epoch_time(event_date)

        type = EventType.get_obj_for_string(type)
        status = EventStatusType.get_obj_for_string(status)

        event: Event = Event.create(name, description, event_date, type, max_seats, status)

        booking_windows = request_data.get("booking_windows", [])
        if booking_windows:
            booking_windows = _create_booking_windows(booking_windows, event)

        categories = request_data.get("categories", [])
        if categories:
            categories = _create_categories(categories, event)

        location = request_data.get("location")
        if location:
            location = _create_location(location)
            event.set_location(location=location)

        event.save()

        price_plans = request_data.get("price_plans")
        if price_plans:
            price_plans = _create_price_plans(price_plans, event)

        event.save()

    if serialized:
        return EventSerializer(event, many=False).data
    return event


def svc_event_get_all_events_for_admin(serialized: bool = True) -> Union["Event", List[dict]]:
    events = Event.objects.all()

    if serialized:
        return EventSerializer(events, many=True).data
    return events


def svc_event_get_event_for_admin(event_id: uuid.UUID, serialized: bool = True) -> Union["Event", dict]:
    event = Event.objects.get(external_id=event_id)

    if serialized:
        return EventSerializer(event, many=False).data
    return event


def svc_event_get_all_events_for_user(serialized: bool = True) -> Union["Event", List[dict]]:
    events = Event.objects.all()

    if serialized:
        return EventUserSerializer(events, many=True).data
    return events


def svc_event_get_event_for_user(event_id: uuid.UUID, serialized: bool = True) -> Union["Event", dict]:
    event = Event.objects.get(external_id=event_id)

    if serialized:
        return EventUserSerializer(event, many=False).data
    return event


def svc_event_update_event_details(
    request_data: dict, event_id: uuid.UUID, serialized: bool = True
) -> Union["Event", dict]:
    with transaction.atomic():
        event = Event.objects.get(external_id=event_id)  # throws ObjectDoesNot exist exception

        if "name" in request_data:
            event.set_name(request_data["name"])

        if "description" in request_data:
            event.set_description(request_data["description"])

        if "event_date" in request_data:
            event_date = _get_datetime_for_epoch_time(request_data["event_date"])
            event.set_event_date(event_date)

        if "type" in request_data:
            event.set_type(request_data["type"])

        if "max_seats" in request_data:
            event.set_available_seats(request_data["max_seats"])

        if "status" in request_data:
            event.set_status(request_data["status"])

        if "location" in request_data:
            location = event.get_location()

            name = request_data["location"].get("name", "")
            address = request_data["location"].get("address", "")
            city = request_data["location"].get("city", "")
            state = request_data["location"].get("state", "")

            location.set_name(name)
            location.set_name(address)
            location.set_name(city)
            location.set_name(state)

            location.save()

        if "booking_windows" in request_data:
            BookingWindow.objects.filter(event=event).delete()

            _create_booking_windows(request_data["booking_windows"], event)

        if "categories" in request_data:
            Category.objects.filter(event=event).delete()

            _create_categories(request_data["categories"], event)

        if "price_plans" in request_data:
            PricePlan.objects.filter(event=event).delete()

            _create_price_plans(request_data["price_plans"], event)

        event.save()

    if serialized:
        return EventSerializer(event, many=False).data
    return event


def svc_event_book_ticket(
    request_data: dict, user: User, event_id: uuid.UUID, serialized: bool = True
) -> Union["Ticket", dict]:
    event = Event.objects.get(external_id=event_id)

    if "ticket_count" not in request_data:
        raise ValueError("ticket_count missing in request_data")

    ticket_count = request_data["ticket_count"]
    if ticket_count <= 0:
        raise ValueError("provide valid ticket_count")

    available_seats = event.get_available_seats()

    if ticket_count > available_seats:
        raise ValueError("ticket_count is greater than available seats")

    ticket = Ticket.objects.create(user=user, event=event)

    event.set_available_seats(available_seats - ticket_count, save=True)

    if serialized:
        return TicketSerializer(ticket, many=False).data
    return ticket


def svc_event_get_booked_tickets_for_event(
    user: User, event_id: uuid.UUID, serialized: bool = True
) -> Union["Ticket", List[dict]]:
    ticket = Ticket.objects.filter(event__external_id=event_id, user=user)

    if serialized:
        return TicketSerializer(ticket, many=True).data
    return ticket


def svc_event_get_all_booked_tickets_of_a_user(user: User, serialized: bool = True) -> Union["Ticket", List[dict]]:
    tickets = Ticket.objects.filter(user=user)

    if serialized:
        return TicketSerializer(tickets, many=True).data
    return tickets
