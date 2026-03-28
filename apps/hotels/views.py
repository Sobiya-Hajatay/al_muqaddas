from django.shortcuts import render, get_object_or_404, redirect
from .models import RoomType
from apps.bookings.models import Booking
from datetime import datetime
from .models import Hotel, RoomType

# def booking_room(request, id):
#     room = get_object_or_404(RoomType, id=id)

#     if request.method == "POST":

#         name = request.POST.get("name")
#         phone = request.POST.get("phone")
#         email = request.POST.get("email")
#         checkin = request.POST.get("checkin")
#         checkout = request.POST.get("checkout")

#         if not all([name, phone, checkin, checkout]):
#             return redirect(request.path)

#         checkin_date = datetime.strptime(checkin, "%Y-%m-%d")
#         checkout_date = datetime.strptime(checkout, "%Y-%m-%d")
#         nights = (checkout_date - checkin_date).days

#         total_amount = nights * float(room.price_per_night)

#         # ✅ FIXED BOOKING (minimal compatible)
#         booking = Booking.objects.create(
#             full_name=name,
#             phone=phone,
#             email=email,
#             persons=1,  # default
#             travel_date=checkin,
#             price_per_person=room.price_per_night,
#             total_amount=total_amount,
#             booking_status="pending",
#             payment_status="unpaid"
#         )

#         request.session["booking_id"] = booking.id

#         return redirect("payment_page", booking_id=booking.id)

#     return render(request, "booking_form_room.html", {"room": room})
def hotel_rooms(request, id):
    
    hotel = get_object_or_404(Hotel, id=id)
    rooms = RoomType.objects.filter(hotel=hotel, is_active=True)

    return render(request, "rooms.html", {
        "hotel": hotel,
        "rooms": rooms
    })
