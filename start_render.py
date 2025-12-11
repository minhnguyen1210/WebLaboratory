"""
Render.com startup script
Chạy cả FastAPI và Flask trong cùng process
"""
import os
import threading
import time
import subprocess
import signal
import sys

# Get port from Render (default 10000)
PORT = int(os.environ.get('PORT', 10000))

fastapi_process = None
flask_process = None

def start_fastapi():
    """Start FastAPI backend on port 8000"""
    global fastapi_process
    print("🚀 Starting FastAPI backend on port 8000...")
    fastapi_process = subprocess.Popen([
        "python", "-m", "uvicorn",
        "huggingface_api:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--workers", "1"
    ])

def start_flask():
    """Start Flask frontend on Render's PORT"""
    global flask_process
    print(f"🚀 Starting Flask frontend on port {PORT}...")
    
    # Set Flask to use Render's PORT
    os.environ['FLASK_RUN_PORT'] = str(PORT)
    os.environ['FLASK_RUN_HOST'] = '0.0.0.0'
    
    flask_process = subprocess.Popen([
        "python", "main.py"
    ])

def cleanup(signum=None, frame=None):
    """Cleanup on exit"""
    print("\n🛑 Shutting down...")
    if fastapi_process:
        fastapi_process.terminate()
    if flask_process:
        flask_process.terminate()
    sys.exit(0)

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

if __name__ == "__main__":
    print("="*60)
    print("🎉 Starting Vietnam Place on Render.com")
    print("="*60)
    
    # Start FastAPI in background thread
    fastapi_thread = threading.Thread(target=start_fastapi, daemon=True)
    fastapi_thread.start()
    time.sleep(5)  # Wait for FastAPI to start
    
    # Start Flask (this will block)
    start_flask()
    
    # Wait for processes
    try:
        if flask_process:
            flask_process.wait()
    except KeyboardInterrupt:
        cleanup()
