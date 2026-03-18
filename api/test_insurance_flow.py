import requests
import os
import json
import time

BACKEND_URL = "http://localhost:8000"
DATA_PATH = r"c:\Users\Soumoditya Das\Downloads\GFG kolkata\InsightPulse_AI\data\Copy of India Life Insurance Claims.csv"

def test_flow():
    # 1. Upload the CSV
    print(f"--- 1. Uploading Data: {os.path.basename(DATA_PATH)} ---")
    with open(DATA_PATH, 'rb') as f:
        files = {'file': (os.path.basename(DATA_PATH), f, 'text/csv')}
        response = requests.post(f"{BACKEND_URL}/upload", files=files)
    
    if response.status_code != 200:
        print(f"Upload failed: {response.text}")
        return
    
    print(f"Upload Success: {response.json().get('message')}")
    
    # 2. Wait a moment for processing if any
    time.sleep(2)
    
    # 3. Chat with J.A.R.V.I.S
    print("\n--- 2. Chatting with J.A.R.V.I.S ---")
    payload = {
        "query": "Analyze the distribution of claim amounts by insurance type",
        "chat_history": []
    }
    response = requests.post(f"{BACKEND_URL}/generate", json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print(f"JARVIS Response (Intent): {data.get('intent')}")
        print(f"SQL Generated: {data.get('sql')}")
        if data.get('error'):
            print(f"ERROR: {data.get('error')}")
        else:
            print("SUCCESS: Received valid dashboard data.")
            print(f"Insights Count: {len(data.get('insights', []))}")
            print(f"Charts Generated: {[c.get('type') for c in data.get('charts', [])]}")
    else:
        print(f"Generation failed: {response.text}")

if __name__ == "__main__":
    test_flow()
