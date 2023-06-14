from django.urls import path
from . import views


app_name = "event"

urlpatterns = [
    path(r"<uuid:event_id>", views.EventAdminDetailView.as_view(), name="handler-event-admin-detail-view"),
    path(r"", views.EventAdminListView.as_view(), name="handler-event-admin-list-view"),
    path(r"user/<uuid:event_id>", views.EventUserDetailView.as_view(), name="handler-event-user-detail-view"),
    path(r"user/", views.EventUserListView.as_view(), name="handler-event-user-list-view"),
    path(r"ticket/bookedtickets", views.UserTicketsView.as_view(), name="handler-user-tickets-view"),
    path(r"ticket/<uuid:event_id>", views.TicketBookingView.as_view(), name="handler-ticket-book-view"),
]
