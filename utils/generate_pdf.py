import tempfile
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.enums import TA_CENTER

PURPLE = colors.HexColor("#6C63FF")
INK    = colors.HexColor("#18181B")
MUTED  = colors.HexColor("#71717A")


def create_pdf(data: dict) -> str:
    info = data.get("personal", {})
    text = data.get("resumeText", "")
    tmp  = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc  = SimpleDocTemplate(tmp.name, pagesize=A4,
                             leftMargin=20*mm, rightMargin=20*mm,
                             topMargin=18*mm, bottomMargin=18*mm)

    name_style    = ParagraphStyle("Name",    fontSize=20, fontName="Helvetica-Bold",  textColor=INK,    alignment=TA_CENTER, spaceAfter=4)
    contact_style = ParagraphStyle("Contact", fontSize=9,  fontName="Helvetica",       textColor=MUTED,  alignment=TA_CENTER, spaceAfter=10)
    section_style = ParagraphStyle("Section", fontSize=11, fontName="Helvetica-Bold",  textColor=PURPLE, spaceBefore=10, spaceAfter=4)
    body_style    = ParagraphStyle("Body",    fontSize=10, fontName="Helvetica",       textColor=INK,    leading=15, spaceAfter=3)
    bullet_style  = ParagraphStyle("Bullet",  fontSize=10, fontName="Helvetica",       textColor=INK,    leading=14, leftIndent=12, spaceAfter=2)

    story = []
    story.append(Paragraph(info.get("name", "Your Name"), name_style))

    contact_parts = [x for x in [info.get("email"), info.get("phone"),
                                   info.get("location"), info.get("linkedin"), info.get("github")] if x]
    story.append(Paragraph("  |  ".join(contact_parts), contact_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PURPLE, spaceAfter=8))

    for line in text.split("\n"):
        line = line.strip()
        if not line:
            story.append(Spacer(1, 4))
            continue
        if line.isupper() or (line.endswith(":") and len(line) < 40):
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#E4E2F0"), spaceBefore=6))
            story.append(Paragraph(line.rstrip(":"), section_style))
        elif line.startswith(("•", "-", "*")):
            story.append(Paragraph(f"• {line.lstrip('•-* ')}", bullet_style))
        else:
            story.append(Paragraph(line, body_style))

    doc.build(story)
    return tmp.name
