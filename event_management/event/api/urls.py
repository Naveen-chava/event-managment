from django.urls import path
from . import views


urlpatterns = [
    path(r"<uuid:event_id>", views.EventDetailView.as_view(), name="handler-event-detail-view"),
    path(r"", views.EventListView.as_view(), name="handler-event-list-view"),
    path(r"user/<uuid:event_id>", views.EventUserDetailView.as_view(), name="handler-event-user-detail-view"),
    path(r"user/", views.EventUserListView.as_view(), name="handler-event-user-list-view"),
    path(r"ticket/bookedtickets", views.UserTicketsView.as_view(), name="handler-ticket-book-view"),
    path(r"ticket/<uuid:event_id>", views.TicketBookingView.as_view(), name="handler-ticket-book-view"),
]
