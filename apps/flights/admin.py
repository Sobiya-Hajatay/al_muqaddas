from django.contrib import admin
from .models import Airline, Airport, Flight


@admin.register(Airline)
class AirlineAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ("code", "city", "country")


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = (
        "airline",
        "flight_number",
        "origin",
        "destination",
        "departure_time",
        "price",
        "available_seats",
    )
    list_filter = ("airline", "origin", "destination")
    search_fields = ("flight_number",)