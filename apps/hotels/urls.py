from django.urls import path
from . import views

urlpatterns = [
    path('hotel/<int:id>/rooms/', views.hotel_rooms, name='hotel_rooms'),
    
    
]