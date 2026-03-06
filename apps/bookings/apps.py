import razorpay
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.apps import AppConfig


class BookingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.bookings'

def payment_success(request):
    if request.method == "POST":
        payment_id = request.POST.get("razorpay_payment_id")
        order_id = request.POST.get("razorpay_order_id")
        signature = request.POST.get("razorpay_signature")
        booking_id = request.POST.get("booking_id")

        booking = get_object_or_404(Booking, id=booking_id)

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        params_dict = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }

        try:
            client.utility.verify_payment_signature(params_dict)

            # ✅ VERIFIED — update booking
            booking.payment_status = "Paid"
            booking.status = "Confirmed"
            booking.razorpay_payment_id = payment_id
            booking.razorpay_order_id = order_id
            booking.razorpay_signature = signature
            booking.save()

            return render(request, "payment_success.html", {"booking": booking})

        except:
            booking.payment_status = "Failed"
            booking.save()
            return render(request, "payment_failed.html")

    return render(request, "payment_failed.html")