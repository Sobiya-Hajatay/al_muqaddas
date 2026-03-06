from django.contrib import admin
from .models import City, Hotel, RoomType


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "country")
    search_fields = ("name",)


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "hotel_type", "star_rating", "is_active")
    list_filter = ("hotel_type", "city", "is_active")
    search_fields = ("name",)


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ("hotel", "name", "price_per_night", "total_rooms", "booked_rooms")
    list_filter = ("hotel",)