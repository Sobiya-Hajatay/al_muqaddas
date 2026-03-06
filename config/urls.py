from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.core.views import contact

from apps.core.views import (
    home,
    hotels_page,
    package_detail,
    book_package,
    admin_dashboard,
    payment_success,   # ⭐ MUST ADD
    download_invoice,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("invoices/", include("apps.invoices.urls")),
    path("accounts/", include("apps.accounts.urls")),

    path('', home, name="home"),
    path("control-room/", admin_dashboard, name="admin_dashboard"),

    # ✅ FLIGHTS APP INCLUDE (VERY IMPORTANT)
   path("flights/", include("apps.flights.urls")),
    path("booking/", include("apps.bookings.urls")),
    path("payment/success/", payment_success, name="payment_success"),
path("invoice/<int:booking_id>/", download_invoice, name="download_invoice"),
 # 💳 Razorpay
    path("payment/success/", payment_success, name="payment_success"),
    path("contact/", contact, name="contact"),

    # 📄 Invoice
    path("invoice/<int:booking_id>/", download_invoice, name="download_invoice"),

    # ✅ HOTELS
    path('hotels/', hotels_page, name="hotels_page"),
path("dashboard/", admin_dashboard, name="admin_dashboard"),

    path('package/<int:pk>/', package_detail, name="package_detail"),
    path('book/<int:pk>/', book_package, name="book_package"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)