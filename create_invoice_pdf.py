from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import black, darkblue

def create_invoice_pdf():
    # Create a new PDF
    c = canvas.Canvas('sample_docs/test_invoice.pdf', pagesize=letter)
    
    # Set up fonts
    c.setFont('Helvetica-Bold', 14)
    
    # Company header
    c.drawString(50, 750, "Beispiel GmbH")
    c.setFont('Helvetica', 12)
    c.drawString(50, 730, "Musterstraße 123")
    c.drawString(50, 710, "10115 Berlin")
    
    # Invoice details
    c.setFont('Helvetica-Bold', 12)
    c.drawString(50, 670, "Rechnung Nr. R2024-002")
    c.setFont('Helvetica', 12)
    c.drawString(50, 650, "Datum: 20. Februar 2024")
    c.drawString(50, 630, "Kundennummer: K-2024-001")
    
    # Main content
    y = 590
    with open('sample_docs/test_invoice.txt', 'r') as f:
        text = f.read()
    
    # Skip the header part we already wrote
    content = text.split('\n\n')[2:]
    for section in content:
        for line in section.split('\n'):
            if line.strip():
                if line.startswith('Gesamt:') or line.startswith('Zwischensumme:') or line.startswith('MwSt.') or line.startswith('Gesamtsumme:'):
                    c.setFont('Helvetica-Bold', 12)
                else:
                    c.setFont('Helvetica', 12)
                c.drawString(50, y, line)
                y -= 15
        y -= 10  # Extra space between sections
    
    # Save the PDF
    c.save()

if __name__ == "__main__":
    create_invoice_pdf() 