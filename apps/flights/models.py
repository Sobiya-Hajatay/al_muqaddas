from django.db import models


class Airline(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="airlines/", blank=True, null=True)

    def __str__(self):
        return self.name


class Airport(models.Model):
    code = models.CharField(max_length=10)  # BOM, JED
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.city} ({self.code})"


class Flight(models.Model):
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)
    flight_number = models.CharField(max_length=20)

    origin = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="departures",
    )
    destination = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="arrivals",
    )

    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    duration = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    available_seats = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["departure_time"]

    def __str__(self):
        return f"{self.airline.name} {self.flight_number}"