import os
import requests
from dotenv import load_dotenv
from googletrans import Translator

# Load environment variables
load_dotenv()

# Set API key directly (for testing)
API_KEY = "sk-bc5d98081d324d36aa0b2c5dd5531faf"

API_URL = "https://api.deepseek.com/v1/chat/completions"

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

def call_deepseek(prompt, system_message=None):
    """
    Call DeepSeek API with a prompt and optional system message.
    
    Args:
        prompt: The user's prompt/question
        system_message: Optional system message to set the context
        
    Returns:
        str: The API response or error message
    """
    try:
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": "deepseek-chat",
            "messages": messages,
            "temperature": 0.3,
            "stream": False
        }

        response = requests.post(API_URL, headers=HEADERS, json=payload)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            print(f"API Error: Status code {response.status_code}")
            print(f"Response: {response.text}")
            return "⚠️ API Error"
    except Exception as e:
        print(f"Error calling DeepSeek API: {str(e)}")
        return "⚠️ API Error"

def translate_to_english(text):
    """Translate text to English using Google Translate."""
    try:
        translator = Translator()
        translation = translator.translate(text, dest='en')
        return translation.text
    except Exception as e:
        print(f"Translation error: {str(e)}")
        return text

def summarize_text(text, max_length=150):
    """
    Create a human-friendly summary of the text in English using DeepSeek.
    
    Args:
        text: The text to summarize
        max_length: Maximum length of the summary in characters
        
    Returns:
        str: The summarized text in English
    """
    try:
        # First translate the text to English
        english_text = translate_to_english(text)
        
        # Create a prompt for DeepSeek
        prompt = f"""Please provide a concise summary of the following text in English.
Keep the summary under {max_length} characters and maintain a professional tone.
Focus on the main points and important details.

Text to summarize:
{english_text}"""

        system_message = """You are an expert at summarizing German business letters and documents.
Your summaries should be clear, concise, and maintain the professional tone of the original text.
Focus on the main points and important details while keeping the summary brief."""

        # Get summary from DeepSeek
        summary = call_deepseek(prompt, system_message)
        
        # Clean up the summary
        summary = summary.strip()
        if not summary.endswith('.'):
            summary += '.'
            
        return summary
    except Exception as e:
        print(f"Error in summarize_text: {str(e)}")
        return "⚠️ Error creating summary"

def extract_key_points(text, max_points=5):
    """
    Extract human-friendly key points from the text in English using DeepSeek.
    
    Args:
        text: The text to analyze
        max_points: Maximum number of key points to extract
        
    Returns:
        list: List of key points in English
    """
    try:
        # First translate the text to English
        english_text = translate_to_english(text)
        
        # Create a prompt for DeepSeek
        prompt = f"""Please extract the {max_points} most important key points from the following text.
Format each point as a clear, concise bullet point.
Focus on the main topics, important dates, and any actions required.

Text to analyze:
{english_text}"""

        system_message = """You are an expert at analyzing German business letters and documents.
Extract the most important points and format them as clear, concise bullet points.
Focus on main topics, important dates, and any required actions."""

        # Get key points from DeepSeek
        key_points_text = call_deepseek(prompt, system_message)
        
        # Split into individual points and clean up
        key_points = [point.strip() for point in key_points_text.split('\n') if point.strip()]
        
        # Ensure each point starts with a bullet
        formatted_points = []
        for point in key_points:
            if not point.startswith('-') and not point.startswith('•'):
                point = f"- {point}"
            formatted_points.append(point)
        
        return formatted_points[:max_points]
    except Exception as e:
        print(f"Error in extract_key_points: {str(e)}")
        return ["⚠️ Error extracting key points"]
