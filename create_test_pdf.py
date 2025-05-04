from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_test_pdf():
    # Create a new PDF
    c = canvas.Canvas('sample_docs/test_letter.pdf', pagesize=letter)
    c.setFont('Helvetica', 12)
    
    # Read the text file
    with open('sample_docs/test_letter.txt', 'r') as f:
        text = f.read()
    
    # Draw text on PDF
    y = 750
    for line in text.split('\n'):
        c.drawString(50, y, line)
        y -= 15
    
    # Save the PDF
    c.save()

if __name__ == "__main__":
    create_test_pdf() 