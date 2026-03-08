from django.shortcuts import render
from apps.bookings.models import Booking

def payment_receipt(request, booking_id):

    booking = Booking.objects.get(id=booking_id)

    return render(request,"payment_receipt.html",{
        "booking": booking
    })