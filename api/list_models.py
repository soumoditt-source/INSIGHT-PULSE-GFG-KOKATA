import os
from google import genai
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path('.env'))

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def list_models():
    print(f"--- Listing Models for Key: {GEMINI_API_KEY[:10]}... ---")
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        for model in client.models.list():
            print(f"- {model.name}")
    except Exception as e:
        print(f"Error listing models: {e}")

if __name__ == "__main__":
    list_models()
