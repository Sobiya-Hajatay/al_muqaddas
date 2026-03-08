from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Min
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

import razorpay

from apps.bookings.models import Booking
from .models import Flight


# ================= FLIGHT LIST =================
def flights_page(request):

    flights = Flight.objects.filter(is_active=True).select_related(
        "airline", "origin", "destination"
    )

    origin = request.GET.get("from_city")
    destination = request.GET.get("to_city")
    sort = request.GET.get("sort")

    if origin:
        flights = flights.filter(origin__city__icontains=origin)

    if destination:
        flights = flights.filter(destination__city__icontains=destination)

    if sort == "price":
        flights = flights.order_by("price")

    elif sort == "duration":
        flights = flights.order_by("duration")

    elif sort == "time":
        flights = flights.order_by("departure_time")

    paginator = Paginator(flights, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    cheapest_price = flights.aggregate(m=Min("price"))["m"]

    context = {
        "flights": page_obj,
        "page_obj": page_obj,
        "from_city": origin,
        "to_city": destination,
        "sort": sort,
        "cheapest_price": cheapest_price,
    }

    return render(request, "flights/flight_list.html", context)


# ================= BOOK FLIGHT =================
@login_required
def book_flight(request, flight_id):

    flight = get_object_or_404(Flight, id=flight_id)

    if request.method == "POST":

        if flight.available_seats <= 0:
            return render(request, "flights/book_flight.html", {
                "flight": flight,
                "error": "No seats available"
            })

        # Razorpay client
        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        amount = int(flight.price) * 100

        # Create Razorpay Order
        order = client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": 1
        })

        # Create Booking
        booking = Booking.objects.create(
            user=request.user,
            flight=flight,
            full_name=request.user.username,
            phone="0000000000",
            email=request.user.email,
            persons=1,
            travel_date=flight.departure_time.date(),
            price_per_person=flight.price,
            razorpay_order_id=order["id"]
        )

        return render(request, "flights/payment.html", {
            "flight": flight,
            "booking": booking,
            "order_id": order["id"],
            "amount": amount,
            "razorpay_key": settings.RAZORPAY_KEY_ID
        })

    return render(request, "flights/book_flight.html", {"flight": flight})


# ================= PAYMENT SUCCESS =================
@csrf_exempt
def payment_success(request):

    if request.method == "POST":

        payment_id = request.POST.get("razorpay_payment_id")
        order_id = request.POST.get("razorpay_order_id")
        signature = request.POST.get("razorpay_signature")

        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        params_dict = {
            "razorpay_payment_id": payment_id,
            "razorpay_order_id": order_id,
            "razorpay_signature": signature
        }

        try:

            # Verify payment signature
            client.utility.verify_payment_signature(params_dict)

            booking = Booking.objects.get(razorpay_order_id=order_id)

            # Update booking payment
            booking.amount_paid = booking.total_amount
            booking.booking_status = "confirmed"

            booking.razorpay_payment_id = payment_id
            booking.razorpay_signature = signature

            booking.save()

            # Reduce seat count
            flight = booking.flight
            flight.available_seats -= booking.persons
            flight.save()

            return redirect("booking_success", booking_id=booking.id)

        except Exception as e:

            return HttpResponse("Payment verification failed")


# ================= BOOKING SUCCESS =================
def booking_success(request, booking_id):

    booking = get_object_or_404(Booking, id=booking_id)

    return render(request, "flights/booking_success.html", {
        "booking": booking
    })