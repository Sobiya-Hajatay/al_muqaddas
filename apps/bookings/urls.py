from django.urls import path
from apps.core.views import book_package
from .views import *
from . import views

urlpatterns = [
    path("book/<int:pk>/", booking_package, name="book_package"),
    path("package/<int:pk>/", package_detail, name="package_detail"),
  path("payment-success/", payment_success, name="payment_success"),
  path('payment/<int:booking_id>/', views.payment_page, name='payment_page'),

]