from django.shortcuts import render, redirect, get_object_or_404
from .models import Booking
from apps.packages.models import Package
from apps.invoices.models import Invoice
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.conf import settings
from django.http import HttpResponseRedirect

# @csrf_exempt
def booking_package(request, pk):

    package = get_object_or_404(Package, id=pk)

    if request.method == "POST":

        persons = int(request.POST.get('guests') or 1)

        booking = Booking.objects.create(
            package=package,
            user=request.user if request.user.is_authenticated else None,  # ✅ FIX
            full_name=request.POST.get('name'),
            phone=request.POST.get('phone'),
            email=request.POST.get('email'),
            persons=persons,
            travel_date=request.POST.get('checkin'),
            price_per_person=package.price
        )

        request.session['booking_id'] = booking.id
        print("REDIRECTING TO PAYMENT 👉", booking.id)

        return HttpResponseRedirect(f"/booking/payment/{booking.id}/")

    return render(request, "booking_form.html", {"package": package})
@csrf_exempt
def payment_success(request):

    if request.method == "POST":

        booking_id = request.POST.get("booking_id")

        booking = Booking.objects.get(id=booking_id)

        booking.payment_status = "paid"
        booking.booking_status = "confirmed"
        booking.razorpay_payment_id = request.POST.get("razorpay_payment_id")
        booking.razorpay_order_id = request.POST.get("razorpay_order_id")
        booking.razorpay_signature = request.POST.get("razorpay_signature")
        booking.save()

        Invoice.objects.get_or_create(
            booking=booking,
            defaults={"amount": booking.total_amount}
        )

        return render(request, "payment_success.html", {"booking": booking})
def payment_page(request, booking_id):

        booking = get_object_or_404(Booking, id=booking_id)

        client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

        amount = int(booking.total_amount * 100)

        order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

        booking.razorpay_order_id = order["id"]
        booking.save()

        return render(request, "payment_page.html", {
        "booking": booking,
        "order_id": order["id"],
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "amount": amount
    })

def package_detail(request, pk):
    package = get_object_or_404(Package, id=pk)

    return render(request, "package_detail.html", {
        "package": package
    })