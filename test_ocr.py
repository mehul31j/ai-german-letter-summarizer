from ocr_utils import extract_text_from_image
import os
import pytesseract
from PIL import Image, ImageDraw, ImageFont
import io

def create_test_image():
    """Create a sample German letter image for testing"""
    # Create a new image with white background
    width, height = 800, 600
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Sample German text
    text = """Sehr geehrte Damen und Herren,

ich schreibe Ihnen bezüglich meiner letzten Rechnung.
Die Rechnung Nr. 12345 vom 15.03.2024 wurde noch nicht beglichen.

Mit freundlichen Grüßen,
Max Mustermann"""
    
    # Add text to image
    try:
        # Try to use a system font
        font = ImageFont.truetype("Arial", 24)
    except:
        # Fallback to default font
        font = ImageFont.load_default()
    
    draw.text((50, 50), text, fill='black', font=font)
    
    # Save the image
    os.makedirs('test_letters', exist_ok=True)
    image_path = 'test_letters/sample_letter.jpg'
    image.save(image_path)
    return image_path

def test_ocr():
    print("Testing OCR configuration...")
    print(f"Tesseract path: {pytesseract.pytesseract.tesseract_cmd}")
    
    # Create test image
    test_image_path = create_test_image()
    print(f"\nCreated test image at: {test_image_path}")
    
    if os.path.exists(test_image_path):
        print("\nTesting OCR on sample letter...")
        try:
            extracted_text = extract_text_from_image(test_image_path)
            print("\nExtracted Text:")
            print("-" * 50)
            print(extracted_text)
            print("-" * 50)
            
            # Display the image
            image = Image.open(test_image_path)
            image.show()
            
        except Exception as e:
            print(f"\nError during OCR processing: {str(e)}")
    else:
        print(f"\nTest image not found at {test_image_path}")
        print("Please add a test image to the test_letters directory")

if __name__ == "__main__":
    test_ocr() 