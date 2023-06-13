from django.contrib import admin

from event.models import Location, Event, BookingWindow, Ticket, Category, PricePlan

models = [Location, Event, BookingWindow, Ticket, Category, PricePlan]
admin.site.register(models)
