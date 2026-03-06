from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Min
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
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

        booking = Booking.objects.create(
            user=request.user,
            flight=flight,
            full_name=request.user.username,
            phone="0000000000",
            email=request.user.email,
            persons=1,
            travel_date=flight.departure_time.date(),
            price_per_person=flight.price
        )

        flight.available_seats -= 1
        flight.save()

        return redirect("booking_success", booking_id=booking.id)

    return render(request, "flights/book_flight.html", {"flight": flight})
def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, "flights/booking_success.html", {"booking": booking})