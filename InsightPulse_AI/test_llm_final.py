import os
import google.generativeai as genai
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path('.env'))

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def test_gemini():
    print(f"--- Testing Native Gemini (Key: {GEMINI_API_KEY[:10]}...) ---")
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        # Use a model name that is known to work
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content("Hello, respond with 'SUCCESS'")
        print(f"Gemini Response: {response.text}")
    except Exception as e:
        print(f"Gemini Error: {e}")

def test_openrouter():
    print(f"\n--- Testing OpenRouter (Key: {OPENROUTER_API_KEY[:10]}...) ---")
    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY,
        )
        # Testing a very reliable free model
        model = "google/gemini-2.0-flash-lite-preview-02-05:free"
        print(f"Attempting {model}...")
        completion = client.chat.completions.create(
          model=model,
          messages=[{"role": "user", "content": "Hello, respond with 'SUCCESS'"}],
        )
        print(f"OpenRouter Response: {completion.choices[0].message.content}")
    except Exception as e:
        print(f"OpenRouter Error: {e}")

if __name__ == "__main__":
    test_gemini()
    test_openrouter()
