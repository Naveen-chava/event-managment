import uuid

from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

from common.permissions import IsAdminUser
from services.event import (
    svc_event_create_event,
    svc_event_get_all_events_for_admin,
    svc_event_update_event_details,
    svc_event_get_event_for_admin,
    svc_event_get_all_events_for_user,
    svc_event_get_event_for_user,
    svc_event_book_ticket,
    svc_event_get_booked_tickets_for_event,
    svc_event_get_all_booked_tickets_of_a_user,
)
from event.models import Event


class EventListView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request, **kwargs):
        try:
            return Response(svc_event_create_event(request_data=request.data), status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, **kwargs):  # get all events
        try:
            return Response(svc_event_get_all_events_for_admin(), status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class EventDetailView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def put(self, request, event_id, **kwargs):
        try:
            return Response(
                svc_event_update_event_details(request_data=request.data, event_id=event_id), status=status.HTTP_200_OK
            )
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, event_id, **kwargs):
        try:
            return Response(svc_event_get_event_for_admin(event_id=event_id), status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Event.DoesNotExist as e:
            return Response({"message": "Invalid event_id"}, status=status.HTTP_400_BAD_REQUEST)


class EventUserListView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, **kwargs):  # get all events for user
        try:
            return Response(svc_event_get_all_events_for_user(), status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class EventUserDetailView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, event_id, **kwargs):  # get all events for user
        try:
            return Response(svc_event_get_event_for_user(event_id=event_id), status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Event.DoesNotExist as e:
            return Response({"message": "Invalid event_id"}, status=status.HTTP_400_BAD_REQUEST)


class TicketBookingView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request, event_id: uuid.UUID, **kwargs):
        try:
            return Response(svc_event_book_ticket(request.data, request.user, event_id), status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, event_id: uuid.UUID, **kwargs):
        try:
            return Response(svc_event_get_booked_tickets_for_event(request.user, event_id), status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserTicketsView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, **kwargs):
        try:
            return Response(svc_event_get_all_booked_tickets_of_a_user(request.user), status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
