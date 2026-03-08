from django.urls import path
from . import views

urlpatterns = [

    path("receipt/<int:booking_id>/", views.payment_receipt, name="payment_receipt"),

]