from django.db import models


class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}, {self.country}" if self.country else self.name


class Hotel(models.Model):
    HOTEL_TYPE = (
        ("budget", "Budget"),
        ("standard", "Standard"),
        ("premium", "Premium"),
        ("luxury", "Luxury"),
    )

    name = models.CharField(max_length=255)
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name="hotels"
    )

    hotel_type = models.CharField(max_length=20, choices=HOTEL_TYPE)
    star_rating = models.PositiveIntegerField(default=3)

    address = models.TextField(blank=True)
    description = models.TextField(blank=True)

    main_image = models.ImageField(upload_to="hotels/", blank=True, null=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class RoomType(models.Model):
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name="rooms"
    )

    name = models.CharField(max_length=100)  # Deluxe, Quad etc
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)

    total_rooms = models.PositiveIntegerField(default=0)
    booked_rooms = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    def available_rooms(self):
        return self.total_rooms - self.booked_rooms

    def __str__(self):
        return f"{self.hotel.name} - {self.name}"