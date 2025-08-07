import markdown2
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from bs4 import BeautifulSoup
import tempfile

def generate_pdf(markdown_text):
    html = markdown2.markdown(markdown_text)
    soup = BeautifulSoup(html, 'html.parser')

    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as pdf_file:
        pdf_path = pdf_file.name

    doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    story = []

    # Custom styles
    h1 = ParagraphStyle('H1', parent=styles['Heading1'], fontSize=16, textColor=colors.HexColor("#2c3e50"), spaceAfter=10)
    h2 = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor("#2c3e50"), spaceAfter=8)
    body = ParagraphStyle('Body', parent=styles['BodyText'], fontSize=10, leading=14, spaceAfter=6)
    blockquote = ParagraphStyle('Quote', parent=body, backColor="#fff3cd", borderPadding=5, leftIndent=10, textColor=colors.HexColor("#856404"))
    code_style = ParagraphStyle('Code', parent=body, fontName="Courier", backColor="#f4f4f4", textColor=colors.HexColor("#d63384"))

    for tag in soup:
        if tag.name == 'h1':
            story.append(Paragraph(tag.text, h1))
        elif tag.name == 'h2':
            story.append(Paragraph(tag.text, h2))
        elif tag.name == 'p':
            story.append(Paragraph(tag.text, body))
        elif tag.name == 'ul':
            items = [ListItem(Paragraph(li.text, body)) for li in tag.find_all('li')]
            story.append(ListFlowable(items, bulletType='bullet'))
        elif tag.name == 'blockquote':
            story.append(Paragraph(tag.text, blockquote))
        elif tag.name == 'code':
            story.append(Paragraph(tag.text, code_style))
        elif tag.name == 'table':
            data = []
            for row in tag.find_all('tr'):
                data.append([cell.get_text() for cell in row.find_all(['td', 'th'])])
            table = Table(data)
            table.setStyle(TableStyle([
                ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4CAF50")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ]))
            story.append(table)

        story.append(Spacer(1, 8))

    doc.build(story)
    return pdf_path
