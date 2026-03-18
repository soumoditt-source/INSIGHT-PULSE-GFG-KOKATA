import os
from google import genai
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path('.env'))

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def test_gemini_3():
    print(f"--- Testing Gemini 3 Pro (Key: {GEMINI_API_KEY[:10]}...) ---")
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        print("Client initialized. Sending request to gemini-3-pro-preview...")
        response = client.models.generate_content(
            model='models/gemini-3-pro-preview',
            contents="Explain why 42 is the answer to life in one sentence."
        )
        
        print("\n--- RESPONSE ---")
        if response.text:
            print(f"TEXT: {response.text}")
        else:
            print("TEXT IS EMPTY")
            if response.candidates:
                print(f"Finish Reason: {response.candidates[0].finish_reason}")
                print(f"Safety Ratings: {response.candidates[0].safety_ratings}")
        
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")

if __name__ == "__main__":
    test_gemini_3()
