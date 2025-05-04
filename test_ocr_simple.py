from ocr_utils import extract_text_from_image
import os

def test_ocr():
    test_image_path = "test_letters/sample_letter.jpg"
    
    if os.path.exists(test_image_path):
        print("Testing OCR on sample letter...")
        extracted_text = extract_text_from_image(test_image_path)
        print("\nExtracted Text:")
        print("-" * 50)
        print(extracted_text)
        print("-" * 50)
    else:
        print(f"Test image not found at {test_image_path}")
        print("Please run create_test_image.py first")

if __name__ == "__main__":
    test_ocr() 