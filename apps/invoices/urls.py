from django.urls import path
from . import views

urlpatterns = [
    path("download/<int:invoice_id>/", views.download_invoice, name="download_invoice"),
]