from ocr_utils import extract_text
import os

def test_pdf_ocr():
    test_pdf_path = "test_letters/sample_letter.pdf"
    
    if os.path.exists(test_pdf_path):
        print("Testing PDF OCR on sample letter...")
        extracted_text = extract_text(test_pdf_path)
        print("\nExtracted Text:")
        print("-" * 50)
        print(extracted_text)
        print("-" * 50)
    else:
        print(f"Test PDF not found at {test_pdf_path}")
        print("Please add a sample PDF to test with")

if __name__ == "__main__":
    test_pdf_ocr() 