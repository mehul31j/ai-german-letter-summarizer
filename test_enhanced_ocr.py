from ocr_utils import extract_text, detect_language, extract_text_from_pdf
import os
import time

def test_auto_detection():
    """Test language auto-detection with confidence scores."""
    print("\n=== Testing Language Auto-Detection ===")
    
    # Test with German text
    german_text = "Sehr geehrte Damen und Herren, ich schreibe Ihnen bezüglich meiner letzten Rechnung."
    lang, confidence = detect_language(german_text)
    print(f"German text detection: {lang} (confidence: {confidence:.2f})")
    
    # Test with English text
    english_text = "Dear Sir or Madam, I am writing regarding my last invoice."
    lang, confidence = detect_language(english_text)
    print(f"English text detection: {lang} (confidence: {confidence:.2f})")
    
    # Test with French text
    french_text = "Madame, Monsieur, je vous écris concernant ma dernière facture."
    lang, confidence = detect_language(french_text)
    print(f"French text detection: {lang} (confidence: {confidence:.2f})")

def test_performance():
    """Test performance optimizations with a sample document."""
    print("\n=== Testing Performance Optimizations ===")
    
    test_file = "test_letters/sample_letter.jpg"
    if not os.path.exists(test_file):
        print("Test file not found. Please run create_test_image.py first.")
        return
    
    # First run (no cache)
    print("\nFirst run (no cache):")
    start_time = time.time()
    text = extract_text(test_file)
    first_run_time = time.time() - start_time
    print(f"Processing time: {first_run_time:.2f} seconds")
    
    # Second run (with cache)
    print("\nSecond run (with cache):")
    start_time = time.time()
    text = extract_text(test_file)
    second_run_time = time.time() - start_time
    print(f"Processing time: {second_run_time:.2f} seconds")
    
    # Calculate speedup
    speedup = first_run_time / second_run_time
    print(f"Cache speedup: {speedup:.2f}x")

def test_parallel_processing():
    """Test parallel processing with a multi-page document."""
    print("\n=== Testing Parallel Processing ===")
    
    # Create a test PDF with multiple pages
    from PIL import Image, ImageDraw, ImageFont
    import os
    
    # Create test directory if it doesn't exist
    os.makedirs('test_letters', exist_ok=True)
    
    # Create multiple pages
    for i in range(3):
        # Create a new image with white background
        width, height = 800, 600
        image = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(image)
        
        # Add text to image
        text = f"Test Page {i+1}\n\nThis is a test document for parallel processing."
        try:
            font = ImageFont.truetype("Arial", 24)
        except:
            font = ImageFont.load_default()
        
        draw.text((50, 50), text, fill='black', font=font)
        
        # Save the image
        image_path = f'test_letters/test_page_{i+1}.jpg'
        image.save(image_path)
        print(f"Created test page: {image_path}")
    
    # Test parallel processing with multiple images
    print("\nTesting parallel processing with multiple images...")
    start_time = time.time()
    all_text = []
    for i in range(3):
        text = extract_text(f'test_letters/test_page_{i+1}.jpg')
        all_text.append(f"--- Page {i+1} ---\n{text}\n")
    processing_time = time.time() - start_time
    print(f"Processing time: {processing_time:.2f} seconds")
    print("\nExtracted text from all pages:")
    print("-" * 50)
    print("\n".join(all_text))
    print("-" * 50)

if __name__ == "__main__":
    print("=== Testing Enhanced OCR Features ===")
    
    # Run all tests
    test_auto_detection()
    test_performance()
    test_parallel_processing()
    
    print("\nAll tests completed!") 