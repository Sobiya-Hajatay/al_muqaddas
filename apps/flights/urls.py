from django.urls import path
from . import views

urlpatterns = [
    path("", views.flights_page, name="flights_page"),
    path("book/<int:flight_id>/", views.book_flight, name="book_flight"),
    path("success/<int:booking_id>/", views.booking_success, name="booking_success"),
    
]