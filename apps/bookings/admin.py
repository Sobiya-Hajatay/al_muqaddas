from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "booking_ref",
        "package",
        "full_name",
        "phone",
        "persons",
        "total_amount",
        "payment_status",
        "booking_status",
        "created_at",
    )

    search_fields = (
        "booking_ref",
        "full_name",
        "phone",
        "email",
    )

    list_filter = (
        "booking_status",
        "payment_status",
        "created_at",
    )

    ordering = ("-created_at",)