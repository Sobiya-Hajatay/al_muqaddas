from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from apps.bookings.models import Booking


from apps.accounts.models import User

if not User.objects.filter(username="admin").exists():
    user = User.objects.create(username="admin", email="admin@gmail.com")
    user.set_password("admin123")
    user.is_superuser = True
    user.is_staff = True
    user.save()


def user_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:

            login(request, user)
            return redirect("dashboard")

        else:

            messages.error(request, "Invalid Username or Password")
            return redirect("login")

    return render(request, "accounts/login.html")

@login_required
def dashboard(request):

    bookings = Booking.objects.filter(user=request.user)

    return render(request, "dashboard.html", {"bookings": bookings})


def user_logout(request):

    logout(request)

    return redirect("login")