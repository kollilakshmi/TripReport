from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)

styles = getSampleStyleSheet()


def create_pdf(filename, trips):

    total = sum(int(trip["amount"]) for trip in trips)

    pdf = SimpleDocTemplate(filename)

    elements = []

    title = Paragraph("<b>SANNI BABU VEHICLE'S TRIPS (AP31 TQ 2107)</b>", styles["Heading2"])
    elements.append(title)
    elements.append(Spacer(1, 20))

    data = [["Date", "Work", "Amount"]]

    for trip in trips:

        data.append([
            trip["date"],
            Paragraph(trip["work"], styles["BodyText"]),
            str(trip["amount"])
        ])

    table = Table(data, colWidths=[80, 320, 80])

    table.setStyle(TableStyle([

        ("GRID", (0,0), (-1,-1), 1, colors.black),

        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),

        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),

        ("ALIGN", (0,0), (-1,-1), "CENTER"),

        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),

        ("BOTTOMPADDING", (0,0), (-1,0), 10)

    ]))

    elements.append(table)

    elements.append(Spacer(1,20))

    total_text = Paragraph(
        f"<b>TOTAL AMOUNT - {total}</b>",
        styles["Heading3"]
    )

    elements.append(total_text)

    pdf.build(elements)