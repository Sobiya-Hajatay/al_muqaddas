from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.core.views import contact
from apps.core import views


from apps.core.views import (
    home,
    hotels_page,
    
    

    admin_dashboard,
    payment_success,   
    download_invoice,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path("", home, name="home"),

    path("accounts/", include("apps.accounts.urls")),
    path("invoices/", include("apps.invoices.urls")),
    path("payments/", include("apps.payments.urls")),
    path("flights/", include("apps.flights.urls")),
    path("booking/", include("apps.bookings.urls")),
    path("", include("apps.core.urls")),   # ✅ MAIN BOOKING FLOW

    path("contact/", contact, name="contact"),
    path("control-room/", admin_dashboard, name="admin_dashboard"),

    # # Packages
    # path('package/<int:pk>/', package_detail, name="package_detail"),

    # Hotels
    path('hotels/', hotels_page, name="hotels_page"),
    path("hotel/<int:id>/rooms/", views.hotel_rooms, name="hotel_rooms"),
    path('book-room/<int:id>/', views.booking_room, name='book_room'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)