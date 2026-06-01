from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)

from reportlab.lib.styles import getSampleStyleSheet

def export_eda_report_pdf(
        report_data,
        output_path="eda_report.pdf"
    ):

    doc = SimpleDocTemplate(output_path)

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph(
        "EDA Analysis Report",
        styles["Title"]
    )

    elements.append(title)

    elements.append(
        Spacer(1, 12)
    )

    for section, content in report_data.items():

        heading = Paragraph(
            section,
            styles["Heading2"]
        )

        body = Paragraph(
            str(content).replace("\n", "<br/>"),
            styles["BodyText"]
        )

        elements.append(heading)

        elements.append(body)

        elements.append(
            Spacer(1, 12)
        )

    doc.build(elements)

    return output_path