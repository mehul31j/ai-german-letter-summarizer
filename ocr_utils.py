import pytesseract
from PIL import Image
import io
import os
from pdf2image import convert_from_path, convert_from_bytes
import tempfile
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache
import time
from tqdm import tqdm

# Set Tesseract path for macOS
if os.path.exists('/opt/homebrew/bin/tesseract'):
    pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

# Set seed for consistent language detection
DetectorFactory.seed = 0

# Language mapping for Tesseract
LANGUAGE_MAPPING = {
    'de': 'deu',  # German
    'en': 'eng',  # English
    'fr': 'fra',  # French
    'es': 'spa',  # Spanish
    'it': 'ita',  # Italian
    'nl': 'nld',  # Dutch
    'pt': 'por',  # Portuguese
    'ru': 'rus',  # Russian
}

# Cache for OCR results
@lru_cache(maxsize=100)
def cached_ocr(image_path, lang):
    """Cache OCR results to avoid reprocessing the same image."""
    return pytesseract.image_to_string(Image.open(image_path), lang=lang)

def get_available_languages():
    """Get list of available Tesseract languages."""
    try:
        return pytesseract.get_languages()
    except Exception as e:
        print(f"Error getting available languages: {str(e)}")
        return ['eng']  # Default to English if can't get languages

def detect_language(text, confidence_threshold=0.3):
    """
    Detect the language of the given text with confidence.
    
    Args:
        text: Text to detect language from
        confidence_threshold: Minimum confidence for language detection
        
    Returns:
        tuple: (language_code, confidence)
    """
    try:
        if not text.strip():
            return 'en', 0.0  # Default to English if text is empty
        
        # Try to detect language with confidence
        from langdetect import detect_langs
        detections = detect_langs(text)
        
        if not detections:
            return 'en', 0.0
        
        # Get the most confident detection
        best_detection = detections[0]
        if best_detection.prob >= confidence_threshold:
            lang = best_detection.lang
            if lang in LANGUAGE_MAPPING:
                return lang, best_detection.prob
        
        return 'en', best_detection.prob  # Default to English if not confident enough
    except LangDetectException:
        return 'en', 0.0

def process_image_page(args):
    """Process a single image page for parallel processing."""
    image_path, lang, page_num = args
    try:
        # Use cached OCR if available
        text = cached_ocr(image_path, lang)
        return page_num, text
    except Exception as e:
        print(f"Error processing page {page_num}: {str(e)}")
        return page_num, ""

def extract_text_from_pdf(file, dpi=300, lang=None, max_workers=4):
    """
    Extract text from a PDF file with parallel processing.
    
    Args:
        file: File object or file path
        dpi: Resolution for PDF to image conversion (default: 300)
        lang: Language code (e.g., 'de', 'en'). If None, will auto-detect.
        max_workers: Number of parallel workers for processing pages
    
    Returns:
        str: Extracted text from all pages
    """
    try:
        start_time = time.time()
        print("Starting PDF processing...")
        
        # Create a temporary directory for storing images
        with tempfile.TemporaryDirectory() as temp_dir:
            # Convert PDF to images
            if isinstance(file, (str, bytes)):
                if isinstance(file, str):
                    images = convert_from_path(file, dpi=dpi)
                else:
                    images = convert_from_bytes(file, dpi=dpi)
            else:
                # If it's a file object (like from Streamlit)
                file_bytes = file.read()
                images = convert_from_bytes(file_bytes, dpi=dpi)
            
            print(f"Converted PDF to {len(images)} images")
            
            # Save images and prepare for parallel processing
            image_paths = []
            for i, image in enumerate(images):
                temp_image_path = os.path.join(temp_dir, f'page_{i+1}.jpg')
                image.save(temp_image_path, 'JPEG')
                image_paths.append(temp_image_path)
            
            # If language is not specified, detect it from the first page
            if lang is None:
                initial_text = cached_ocr(image_paths[0], 'eng')
                lang, confidence = detect_language(initial_text)
                print(f"Detected language: {lang} (confidence: {confidence:.2f})")
            
            # Map to Tesseract language code
            tesseract_lang = LANGUAGE_MAPPING.get(lang, 'eng')
            
            # Process pages in parallel
            print("Processing pages in parallel...")
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                # Prepare arguments for parallel processing
                args = [(path, tesseract_lang, i+1) for i, path in enumerate(image_paths)]
                
                # Submit tasks and track progress
                futures = [executor.submit(process_image_page, arg) for arg in args]
                results = []
                
                # Process results as they complete
                for future in tqdm(as_completed(futures), total=len(futures), desc="Processing pages"):
                    page_num, text = future.result()
                    results.append((page_num, text))
            
            # Sort results by page number and combine text
            results.sort(key=lambda x: x[0])
            all_text = [f"--- Page {page_num} ---\n{text}\n" for page_num, text in results]
            
            processing_time = time.time() - start_time
            print(f"PDF processing completed in {processing_time:.2f} seconds")
            
            return "\n".join(all_text)
            
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
        return ""

def extract_text_from_image(file, lang=None):
    """
    Extract text from an image file with auto-detection.
    
    Args:
        file: File object or file path
        lang: Language code (e.g., 'de', 'en'). If None, will auto-detect.
    
    Returns:
        str: Extracted text
    """
    try:
        # Handle file object (like from Streamlit)
        if hasattr(file, 'read'):
            image = Image.open(io.BytesIO(file.read()))
        else:
            # Handle file path
            image = Image.open(file)
        
        # First extraction with default language
        initial_text = pytesseract.image_to_string(image, lang='eng')
        
        # If language is not specified, detect it
        if lang is None:
            lang, confidence = detect_language(initial_text)
            print(f"Detected language: {lang} (confidence: {confidence:.2f})")
        
        # Map to Tesseract language code
        tesseract_lang = LANGUAGE_MAPPING.get(lang, 'eng')
        
        # Extract text using detected/specified language
        text = pytesseract.image_to_string(image, lang=tesseract_lang)
        
        # Clean up the text
        text = text.strip()
        
        return text
        
    except Exception as e:
        print(f"Error in OCR: {str(e)}")
        print(f"Tesseract path: {pytesseract.pytesseract.tesseract_cmd}")
        return ""

def extract_text(file, lang=None):
    """
    Extract text from a file (image or PDF) with auto-detection.
    
    Args:
        file: File object or file path
        lang: Language code (e.g., 'de', 'en'). If None, will auto-detect.
    
    Returns:
        str: Extracted text
    """
    # Check if the file is a PDF
    if isinstance(file, str):
        if file.lower().endswith('.pdf'):
            return extract_text_from_pdf(file, lang=lang)
    elif hasattr(file, 'name') and file.name.lower().endswith('.pdf'):
        return extract_text_from_pdf(file, lang=lang)
    
    # If not a PDF, treat as image
    return extract_text_from_image(file, lang=lang)