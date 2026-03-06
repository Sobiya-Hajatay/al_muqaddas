from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import Table
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from django.shortcuts import get_object_or_404
from .models import Invoice


def download_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.invoice_number}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()
    elements.append(Paragraph("AL MUQADDAS TOURS & TRAVELS", styles["Title"]))
    elements.append(Spacer(1, 0.3 * inch))

    data = [
        ["Invoice No:", invoice.invoice_number],
        ["Booking Ref:", invoice.booking.booking_ref],
        ["Customer:", invoice.booking.full_name],
        ["Phone:", invoice.booking.phone],
        ["Package:", invoice.booking.package.title],
        ["Amount:", f"₹ {invoice.amount}"],
    ]

    table = Table(data, colWidths=[150, 300])
    elements.append(table)

    doc.build(elements)
    return response