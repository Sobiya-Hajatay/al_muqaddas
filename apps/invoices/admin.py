from django.contrib import admin
from .models import Invoice


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("invoice_number", "booking", "amount", "issued_at")
    search_fields = ("invoice_number", "booking__booking_ref")