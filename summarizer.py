import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")

API_URL = "https://api.deepseek.com/v1/chat/completions"  # confirm with latest docs

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

def call_deepseek(prompt):
    payload = {
        "model": "deepseek-chat",  # or deepseek-coder if you're using it
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that summarizes German letters and extracts key points."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        print("Error:", response.text)
        return "⚠️ API Error"

def summarize_text(text):
    prompt = f"Fasse diesen offiziellen deutschen Brief in einfachen Worten zusammen:\n\n{text}"
    return call_deepseek(prompt)

def extract_key_points(text):
    prompt = f"Liste die wichtigsten Informationen und Handlungspunkte aus diesem deutschen Brief als Bullet Points auf:\n\n{text}"
    output = call_deepseek(prompt)
    return output.split("\n")  # Assuming bullet points
