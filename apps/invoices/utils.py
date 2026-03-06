import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from django.conf import settings


def generate_invoice_pdf(invoice):
    """
    Generate PDF invoice file and save to media/invoices/
    """

    # folder create
    invoice_dir = os.path.join(settings.MEDIA_ROOT, "invoices")
    os.makedirs(invoice_dir, exist_ok=True)

    file_path = os.path.join(invoice_dir, f"{invoice.invoice_number}.pdf")

    doc = SimpleDocTemplate(file_path, pagesize=A4)
    styles = getSampleStyleSheet()

    elements = []

    # ===== Title =====
    elements.append(Paragraph("AL MUQADDAS TOURS & TRAVELS", styles["Title"]))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Invoice No: {invoice.invoice_number}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    booking = invoice.booking

    data = [
        ["Customer Name", booking.full_name],
        ["Phone", booking.phone],
        ["Package", booking.package.title],
        ["Travel Date", str(booking.travel_date)],
        ["Persons", str(booking.persons)],
        ["Amount", f"₹ {invoice.amount}"],
    ]

    table = Table(data, colWidths=[200, 300])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.white),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))

    elements.append(table)
    doc.build(elements)

    return f"invoices/{invoice.invoice_number}.pdf"