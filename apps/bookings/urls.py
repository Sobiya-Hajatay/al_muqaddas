from django.urls import path
from apps.core.views import book_package, package_detail
from .views import payment_success

urlpatterns = [
    path("book/<int:pk>/", book_package, name="book_package"),
    path("package/<int:pk>/", package_detail, name="package_detail"),
  path("payment-success/", payment_success, name="payment_success"),
]