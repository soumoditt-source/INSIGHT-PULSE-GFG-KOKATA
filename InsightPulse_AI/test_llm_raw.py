import os
from google import genai
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path('.env'))

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def test_gemini_raw():
    print(f"--- Testing Modern Gemini (Key: {GEMINI_API_KEY[:10]}...) ---")
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        print("Client initialized. Sending request...")
        response = client.models.generate_content(
            model='gemini-1.5-pro',
            contents="Respond only with the word 'HELLO WORLD'."
        )
        
        print("\n--- RAW RESPONSE ---")
        print(f"TEXT: {response.text}")
        print(f"FINISH_REASON: {response.candidates[0].finish_reason if response.candidates else 'N/A'}")
        print(f"SAFETY: {response.candidates[0].safety_ratings if response.candidates else 'N/A'}")
        
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_gemini_raw()
