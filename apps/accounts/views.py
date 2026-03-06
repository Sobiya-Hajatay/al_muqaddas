from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
import json
from django.contrib.auth.decorators import login_required
from apps.bookings.models import Booking
from django.shortcuts import render

@login_required
def dashboard(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, "dashboard.html", {"bookings": bookings})


User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        user = User.objects.create_user(
            username=request.data['username'],
            password=request.data['password'],
            phone=request.data['phone']
        )
        return Response({'status': 'registered'})

class LoginView(APIView):
    def post(self, request):
        user = User.objects.get(username=request.data['username'])
        if user.check_password(request.data['password']):
            refresh = RefreshToken.for_user(user)
            return Response({'token': str(refresh.access_token)})
        return Response({'error': 'Invalid credentials'})
