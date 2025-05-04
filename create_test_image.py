from PIL import Image, ImageDraw, ImageFont
import os

def create_test_image():
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
    print(f"Created test image at: {image_path}")
    return image_path

if __name__ == "__main__":
    create_test_image() 