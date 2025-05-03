from transformers import pipeline

translator = pipeline("translation", model="Helsinki-NLP/opus-mt-de-en")

def translate_to_english(text):
    return translator(text)[0]['translation_text']
