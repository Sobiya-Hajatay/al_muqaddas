from django.contrib import admin
from .models import Package, PackageDeparture


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ("title", "package_type", "price", "is_active", "created_at")
    list_filter = ("package_type", "is_active")
    search_fields = ("title",)


@admin.register(PackageDeparture)
class PackageDepartureAdmin(admin.ModelAdmin):
    list_display = (
        "package",
        "departure_date",
        "return_date",
        "total_seats",
        "booked_seats",
        "is_active",
    )
    list_filter = ("is_active", "departure_date")