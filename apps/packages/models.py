from django.db import models


class Package(models.Model):
    PACKAGE_TYPE = (
        ('umrah', 'Umrah'),
        ('hajj', 'Hajj'),
        ('holiday', 'Holiday'),
    )

    title = models.CharField(max_length=255)
    package_type = models.CharField(max_length=20, choices=PACKAGE_TYPE)

    # Base display price (starting from)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    duration = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    image = models.ImageField(upload_to='packages/', blank=True, null=True)

    # Package behavior
    is_group_package = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class PackageDeparture(models.Model):
    package = models.ForeignKey(
        Package,
        on_delete=models.CASCADE,
        related_name="departures"
    )

    departure_date = models.DateField()
    return_date = models.DateField()

    # Seat control
    total_seats = models.PositiveIntegerField(default=0)
    booked_seats = models.PositiveIntegerField(default=0)

    # Pricing structure
    adult_price = models.DecimalField(max_digits=10, decimal_places=2)
    child_with_bed_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    child_without_bed_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    infant_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["departure_date"]

    def available_seats(self):
        return self.total_seats - self.booked_seats

    def __str__(self):
        return f"{self.package.title} - {self.departure_date}"