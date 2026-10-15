
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors

pdf = SimpleDocTemplate("knowledge_base/faq.pdf", pagesize=letter)

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="FAQTitle",
    parent=styles["Title"],
    alignment=TA_CENTER,
    textColor=colors.darkblue,
))
styles.add(ParagraphStyle(
    name="Question",
    parent=styles["Heading2"],
    textColor=colors.darkblue,
    spaceBefore=12,
    spaceAfter=5,
))

content = [
    Paragraph("Customer Support FAQ", styles["FAQTitle"]),
    Spacer(1, 16),

    Paragraph("1. How can I track my order?", styles["Question"]),
    Paragraph(
        "After your order ships, you will receive an email with a tracking link. "
        "Tracking information may take up to 24 hours to appear.",
        styles["BodyText"],
    ),

    Paragraph("2. How long does shipping take?", styles["Question"]),
    Paragraph(
        "Standard shipping usually takes 3–7 business days after dispatch. "
        "Express shipping, when available, usually takes 1–3 business days.",
        styles["BodyText"],
    ),

    Paragraph("3. What is the return policy?", styles["Question"]),
    Paragraph(
        "Unused items in their original condition may be returned within "
        "30 days of delivery. Some products may be excluded.",
        styles["BodyText"],
    ),

    Paragraph("4. How do I get a refund?", styles["Question"]),
    Paragraph(
        "Submit a return request with your order number. Once the returned item "
        "is inspected and approved, refunds typically take 5–10 business days "
        "to process. Bank processing may take longer.",
        styles["BodyText"],
    ),

    Paragraph("5. What if my item arrives damaged?", styles["Question"]),
    Paragraph(
        "Contact customer support with your order number, a description of "
        "the damage, and photos of the item and packaging.",
        styles["BodyText"],
    ),

    Paragraph("6. Can I cancel an order?", styles["Question"]),
    Paragraph(
        "Contact customer support as soon as possible. Cancellation may not "
        "be possible once an order has been processed or shipped.",
        styles["BodyText"],
    ),

    Paragraph("7. What if my package is marked delivered but is missing?",
             styles["Question"]),
    Paragraph(
        "Check your delivery location and confirm the shipping address. "
        "If the package remains missing, contact support with your order number.",
        styles["BodyText"],
    ),
]

pdf.build(content)
print("faq.pdf created successfully!")
