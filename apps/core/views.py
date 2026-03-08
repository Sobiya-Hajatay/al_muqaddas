from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count, Min
from django.db.models.functions import ExtractMonth
from decimal import Decimal
import uuid
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from io import BytesIO
from apps.core.models import ContactMessage
from apps.packages.models import Package
from apps.bookings.models import Booking
from apps.hotels.models import Hotel
from apps.flights.models import Flight
from apps.invoices.models import Invoice
from django.core.mail import send_mail




# ================= HOME =================

def home(request):
    packages = Package.objects.filter(is_active=True)

    city = request.GET.get("city")
    if city:
        packages = packages.filter(title__icontains=city.strip())

    packages = packages.order_by("-created_at")[:6]

    context = {
        "packages": packages,
        "has_packages": packages.exists(),
    }

    return render(request, "home.html", context)


# ================= PACKAGE DETAIL =================
def package_detail(request, pk):
    package = get_object_or_404(Package, id=pk)

    return render(request, "package_detail.html", {
        "package": package
    })


# ================= BOOK PACKAGE =================
def book_package(request, pk):
    package = get_object_or_404(Package, id=pk)

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")

        persons = int(request.POST.get("persons") or 1)
        travel_date = request.POST.get("travel_date")

        if not full_name or not phone or not travel_date:
            messages.error(request, "Please fill required fields.")
            return redirect("book_package", pk=pk)

        # ✅ CREATE BOOKING
        booking = Booking.objects.create(
            user=request.user, 
            package=package,
            full_name=full_name,
            phone=phone,
            email=email,
            persons=persons,
            travel_date=travel_date,
            price_per_person=package.price,
            amount_paid=Decimal("0"),
        )

        # ✅ CREATE INVOICE
        Invoice.objects.get_or_create(
            booking=booking,
            defaults={
                "invoice_number": "INV-" + uuid.uuid4().hex[:8].upper(),
                "amount": booking.total_amount,
            }
        )

        # ===============================
        # ✅ CREATE RAZORPAY ORDER
        # ===============================
        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        order = client.order.create({
            "amount": int(booking.total_amount * 100),
            "currency": "INR",
            "payment_capture": 1,
        })

        request.session["booking_id"] = booking.id

        context = {
            "booking": booking,
            "razorpay_key": settings.RAZORPAY_KEY_ID,
            "order_id": order["id"],
            "amount": int(booking.total_amount * 100),
        }

        return render(request, "payment_page.html", context)

    return render(request, "booking_form.html", {"package": package})


# ================= PAYMENT SUCCESS =================
@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        params_dict = {
            "razorpay_order_id": request.POST.get("razorpay_order_id"),
            "razorpay_payment_id": request.POST.get("razorpay_payment_id"),
            "razorpay_signature": request.POST.get("razorpay_signature"),
        }

        try:
            client.utility.verify_payment_signature(params_dict)

            booking_id = request.session.get("booking_id")
            booking = Booking.objects.get(id=booking_id)

            booking.amount_paid = booking.total_amount
            booking.user = request.user
            booking.save()

            return redirect("booking_success", booking_id=booking.id)

        except Exception:
            return HttpResponse("Payment Failed")


# ================= BOOKING SUCCESS =================
def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    return render(request, "booking_success.html", {
        "booking": booking
    })


# ================= DOWNLOAD INVOICE PDF =================
def download_invoice(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    p.setFont("Helvetica-Bold", 16)
    p.drawString(180, 800, "AL MUQADDAS TOURS & TRAVELS")

    p.setFont("Helvetica", 12)
    p.drawString(50, 750, f"Invoice: {booking.invoice.invoice_number}")
    p.drawString(50, 730, f"Name: {booking.full_name}")
    p.drawString(50, 710, f"Phone: {booking.phone}")
    p.drawString(50, 690, f"Package: {booking.package.title}")
    p.drawString(50, 670, f"Persons: {booking.persons}")
    p.drawString(50, 650, f"Total Amount: ₹{booking.total_amount}")

    p.showPage()
    p.save()

    buffer.seek(0)
    return HttpResponse(buffer, content_type="application/pdf")


# ================= FLIGHTS PAGE =================
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

    cheapest_price = flights.aggregate(m=Min("price"))["m"]

    context = {
        "flights": flights,
        "from_city": origin,
        "to_city": destination,
        "cheapest_price": cheapest_price,
        "sort": sort,
    }

    return render(request, "flights.html", context)


# ================= HOTELS PAGE =================
def hotels_page(request):
    city = request.GET.get("city")
    checkin = request.GET.get("checkin")
    checkout = request.GET.get("checkout")

    hotels = Hotel.objects.filter(is_active=True).select_related("city")

    if city:
        hotels = hotels.filter(city__name__icontains=city)

    context = {
        "city": city,
        "checkin": checkin,
        "checkout": checkout,
        "hotels": hotels,
        "searched": bool(city),
    }

    return render(request, "hotels.html", context)


# ================= ADMIN DASHBOARD =================
@staff_member_required
def admin_dashboard(request):
    total_packages = Package.objects.count()
    total_bookings = Booking.objects.count()

    total_revenue = Booking.objects.aggregate(
        total=Sum("total_amount")
    )["total"] or 0

    latest_bookings = (
        Booking.objects.select_related("package")
        .order_by("-id")[:5]
    )

    monthly_data = (
        Booking.objects
        .annotate(month=ExtractMonth("created_at"))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )

    monthly_labels = [f"Month {x['month']}" for x in monthly_data]
    monthly_counts = [x["count"] for x in monthly_data]

    context = {
        "total_packages": total_packages,
        "total_bookings": total_bookings,
        "total_revenue": total_revenue,
        "latest_bookings": latest_bookings,
        "monthly_labels": monthly_labels,
        "monthly_counts": monthly_counts,
    }

    return render(request, "admin_dashboard.html", context)
def contact(request):

    success = False

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        email_message = f"""
New Contact Message

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}
"""

    try:
        send_mail(
        subject,
        message,
        email,
        ["admin@almuqaddas.in"],
    )
    except:
        pass

    return render(request,"contact.html",{"success":success})
def hotel_rooms(request, id):

    hotel = get_object_or_404(Hotel, id=id)

    rooms = Room.objects.filter(hotel=hotel)

    return render(request, "rooms.html", {
        "hotel": hotel,
        "rooms": rooms
    })
def contact(request):

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        print(name, email, subject, message)  # Debug in terminal

        messages.success(request, "Message sent successfully!")

        return redirect("contact")

    return render(request, "contact.html")
    