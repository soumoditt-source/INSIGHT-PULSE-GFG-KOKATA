"""
InsightPulse AI - One-Command Launcher
Run: python run.py
"""
import subprocess
import sys
import time
import os
import threading
import signal

os.environ["PYTHONIOENCODING"] = "utf-8"

BACKEND_PORT = 8000
FRONTEND_PORT = 8501

def run_backend():
    print("🚀 Starting InsightPulse AI Backend (FastAPI)...")
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    subprocess.run([
        sys.executable, "-m", "uvicorn", "backend:app",
        "--host", "0.0.0.0",
        "--port", str(BACKEND_PORT),
        "--reload"
    ], env=env)

def run_frontend():
    print("🎨 Starting InsightPulse AI Frontend (Streamlit)...")
    time.sleep(2)  # Give backend a head start
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", "app.py",
        "--server.port", str(FRONTEND_PORT),
        "--server.headless", "false",
        "--browser.gatherUsageStats", "false"
    ], env=env)

if __name__ == "__main__":
    print("=" * 60)
    print("  InsightPulse AI - Conversational BI Dashboard")
    print("  Ask. Understand. Act.")
    print("=" * 60)
    print(f"  Backend  -> http://localhost:{BACKEND_PORT}")
    print(f"  Frontend -> http://localhost:{FRONTEND_PORT}")
    print(f"  API Docs -> http://localhost:{BACKEND_PORT}/docs")
    print("=" * 60)

    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    run_frontend()
