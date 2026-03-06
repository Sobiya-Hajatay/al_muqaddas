from django.db import models
import uuid
from apps.packages.models import Package
from django.conf import settings

class Booking(models.Model):

    # ================= STATUS OPTIONS =================
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
    )

    PAYMENT_STATUS = (
        ("unpaid", "Unpaid"),
        ("partial", "Partial"),
        ("paid", "Paid"),
    )

    # ================= CORE =================
    booking_ref = models.CharField(max_length=20, unique=True, blank=True)
    package = models.ForeignKey(
    Package,
    on_delete=models.CASCADE,
    null=True,
    blank=True
)
    user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    null=True,
    blank=True
)
    flight = models.ForeignKey(
    'flights.Flight',
    on_delete=models.CASCADE,
    null=True,
    blank=True
)
   

    # ================= CUSTOMER =================
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    # ================= TRAVEL =================
    persons = models.PositiveIntegerField(default=1)
    travel_date = models.DateField()

    # ================= MONEY =================
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # ================= STATUS =================
    booking_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default="unpaid",
    )

    # ================= RAZORPAY =================
    razorpay_payment_id = models.CharField(max_length=200, blank=True, null=True)
    razorpay_order_id = models.CharField(max_length=200, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=200, blank=True, null=True)

    # ================= META =================
    created_at = models.DateTimeField(auto_now_add=True)

    # ================= AUTO LOGIC =================
    def save(self, *args, **kwargs):

        # Generate booking reference
        if not self.booking_ref:
            self.booking_ref = "AMT" + uuid.uuid4().hex[:8].upper()

        # Auto calculate total
        self.total_amount = (self.price_per_person or 0) * (self.persons or 0)

        # Auto payment status
        if self.amount_paid >= self.total_amount and self.total_amount > 0:
            self.payment_status = "paid"
        elif self.amount_paid > 0:
            self.payment_status = "partial"
        else:
            self.payment_status = "unpaid"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.booking_ref} - {self.full_name}"