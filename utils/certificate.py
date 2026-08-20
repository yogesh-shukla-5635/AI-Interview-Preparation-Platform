from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch
import datetime
import random
import os
import qrcode


def generate_certificate(name, category, score):

    folder = "certificates"

    os.makedirs(folder, exist_ok=True)

    safe_name = name.replace(" ", "_")
    filename = f"{folder}/{safe_name}_certificate.pdf"
    today = datetime.datetime.now().strftime("%d %B %Y")

    certificate_id = f"AI-{datetime.datetime.now().year}-{random.randint(10000,99999)}"
    
    # QR Code Data
    qr_data = (
    f"Certificate ID: {certificate_id}\n"
    f"Name: {name.title()}\n"
    f"Score: {score}/100"
)

# Generate simple, high-quality QR
    qr_image = qrcode.make(
        qr_data,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4
    )

    qr_folder = "certificates/qr"
    os.makedirs(qr_folder, exist_ok=True)

    qr_path = f"{qr_folder}/{certificate_id}.png"
    qr_image.save(qr_path)

    c = canvas.Canvas(filename, pagesize=A4)

    width, height = A4
    # Background Template
    template = "static/images/certificate_template.png"

    if os.path.exists(template):
        c.drawImage(
            ImageReader(template),
            0,
            0,
            width=width,
            height=height
        )

    # Name
    c.setFillColor(HexColor("#0B2E6B"))
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(width/2, 445, name.title())

    # Category
    c.setFillColor(HexColor("#0B2E6B"))

    category_text = f"{category} Mock Interview"
    if len(category_text) > 30:
        c.setFont("Helvetica-Bold", 15)
    else:
        c.setFont("Helvetica-Bold", 18)

    c.drawCentredString(width/2, 355, category_text)


    c.setFillColor(HexColor("#F4C542"))
    c.setFont("Helvetica-Bold", 34)
    c.drawCentredString(width/2 - 22, 252, str(score))

# Date
    c.setFillColor(HexColor("#0B2E6B"))
    c.setFont("Helvetica", 11)
    c.drawString(120, 178, today)

# Certificate ID
    c.drawString(310, 178, certificate_id)
    
    # Functional QR Code
    qr_x = 265
    qr_y = 25
    qr_size = 54
    c.setFillColor(HexColor("#FFFDF6"))
    c.rect(
        263,
        20,
        56,
        56,
        fill=1,
        stroke=0
    )


    c.drawImage(
        qr_path,
        qr_x,
        qr_y,
        width=qr_size,
        height=qr_size,
        preserveAspectRatio=True,
        mask="auto"
    )
    
    c.save()

    return filename