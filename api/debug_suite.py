import requests
import json

def test_diagnostics():
    print("--- TESTING HEALTH ---")
    h = requests.get("http://localhost:8000/health").json()
    print(json.dumps(h, indent=2))

    print("\n--- TESTING PROFILE ---")
    p = requests.get("http://localhost:8000/profile").json()
    mv = p.get("missing_values")
    print(f"Type of missing_values: {type(mv)}")
    print(f"Content: {json.dumps(mv, indent=2)}")

    print("\n--- TESTING CHAT ---")
    payload = {
        "query": "Tell me about the columns in this data.",
        "session_id": "test",
        "chat_history": []
    }
    r = requests.post("http://localhost:8000/generate", json=payload).json()
    print(f"Chat Response Summary: {r.get('error') or 'SUCCESS'}")
    if r.get('error'):
        print(f"Error Message: {r.get('error')}")

if __name__ == "__main__":
    test_diagnostics()
