import razorpay
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from .models import Booking
from apps.invoices.models import Invoice 
def payment_page(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    order_amount = int(booking.total_amount * 100)

    order = client.order.create({
        "amount": order_amount,
        "currency": "INR",
        "payment_capture": 1
    })

    booking.razorpay_order_id = order["id"]
    booking.save()

    context = {
        "booking": booking,
        "order_id": order["id"],
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "amount": order_amount
    }

    return render(request, "payment.html", context)

def payment_success(request):
    if request.method == "POST":
        payment_id = request.POST.get("razorpay_payment_id")
        order_id = request.POST.get("razorpay_order_id")
        signature = request.POST.get("razorpay_signature")
        booking_id = request.POST.get("booking_id")

        booking = get_object_or_404(Booking, id=booking_id)

        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        params_dict = {
            "razorpay_order_id": order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature,
        }

        try:
            client.utility.verify_payment_signature(params_dict)

            # ✅ IMPORTANT FIX
            booking.amount_paid = booking.total_amount
            booking.payment_status = "paid"
            booking.booking_status = "confirmed"

            booking.razorpay_payment_id = payment_id
            booking.razorpay_order_id = order_id
            booking.razorpay_signature = signature
            booking.save()
            Invoice.objects.get_or_create(
                booking=booking,
                defaults={"amount": booking.total_amount}
            )

            return render(request, "payment_success.html", {"booking": booking})

        except Exception as e:
            print("SIGNATURE ERROR:", str(e))
            return render(request, "payment_failed.html")

    return render(request, "payment_failed.html")