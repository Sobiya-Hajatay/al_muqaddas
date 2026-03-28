from django.shortcuts import render
from .models import ContactMessage

def contact(request):

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        return render(request,"contact.html",{"success":True})

    return render(request,"contact.html")
from django.shortcuts import render
from apps.bookings.models import Booking

def payment_success(request):

    payment_id = request.GET.get("payment_id")

    # 🔥 booking session se lao
    booking_id = request.session.get("booking_id")

    booking = None

    if booking_id:
        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            booking = None

    return render(request, "payment_success.html", {
        "payment_id": payment_id,
        "booking": booking
        
    })