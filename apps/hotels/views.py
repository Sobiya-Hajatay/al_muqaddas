from django.shortcuts import render, get_object_or_404
from .models import Hotel, Room

def hotel_rooms(request, id):

    hotel = get_object_or_404(Hotel, id=id)

    rooms = Room.objects.filter(hotel=hotel)

    return render(request, "rooms.html", {
        "hotel": hotel,
        "rooms": rooms
    })