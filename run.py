"""
Script tự động chạy FastAPI + Flask với Ngrok
Chạy: python run_with_ngrok.py
"""

import os
import time
import subprocess
import threading
from pyngrok import ngrok
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Lấy token từ .env
NGROK_TOKEN = os.getenv('NGROK_AUTH_TOKEN')

if not NGROK_TOKEN:
    print("❌ Thiếu NGROK_AUTH_TOKEN trong file .env!")
    print("Hãy thêm dòng: NGROK_AUTH_TOKEN=your_token_here")
    exit(1)

# Set auth token
ngrok.set_auth_token(NGROK_TOKEN)

print("🚀 Starting Vietnam Place with Ngrok...\n")

# ============ FUNCTIONS ============

def start_fastapi():
    """Chạy FastAPI backend"""
    print("📦 Starting FastAPI backend (port 8000)...")
    subprocess.run([
        "python", "-m", "uvicorn", 
        "huggingface_api:app", 
        "--host", "0.0.0.0", 
        "--port", "8000"
    ])

def start_flask():
    """Chạy Flask frontend"""
    print("📦 Starting Flask frontend (port 5000)...")
    subprocess.run(["python", "main.py"])

# ============ START SERVERS ============

# Start FastAPI in background thread
fastapi_thread = threading.Thread(target=start_fastapi, daemon=True)
fastapi_thread.start()
print("✅ FastAPI thread started")
time.sleep(5)  # Đợi FastAPI khởi động

# Expose FastAPI với Ngrok
print("\n🌐 Exposing FastAPI with Ngrok...")
fastapi_tunnel = ngrok.connect(8000, bind_tls=True)
fastapi_url = fastapi_tunnel.public_url
print(f"✅ FastAPI URL: {fastapi_url}")

# Cập nhật huggingface_client.js tự động
print("\n📝 Updating huggingface_client.js...")
with open('huggingface_client.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Thay đổi URL trong constructor
old_line = "constructor(apiBase = 'http://localhost:8000')"
new_line = f"constructor(apiBase = '{fastapi_url}')"
content = content.replace(old_line, new_line)

with open('huggingface_client.js', 'w', encoding='utf-8') as f:
    f.write(content)
print(f"✅ Updated huggingface_client.js with: {fastapi_url}")

# Start Flask in background thread
flask_thread = threading.Thread(target=start_flask, daemon=True)
flask_thread.start()
print("\n✅ Flask thread started")
time.sleep(5)  # Đợi Flask khởi động

# Expose Flask với Ngrok
print("\n🌐 Exposing Flask with Ngrok...")
flask_tunnel = ngrok.connect(5000, bind_tls=True)
flask_url = flask_tunnel.public_url
print(f"✅ Flask URL: {flask_url}")

# ============ SUMMARY ============

print("\n" + "="*60)
print("🎉 ALL SERVICES READY!")
print("="*60)
print(f"📊 FastAPI Backend:  {fastapi_url}")
print(f"🌐 Flask Frontend:   {flask_url}")
print(f"📈 Ngrok Dashboard:  http://127.0.0.1:4040")
print("="*60)
print("\n💡 Share Flask URL with your friends!")
print(f"   👉 {flask_url}")
print("\n⏸️  Press Ctrl+C to stop all services")
print("="*60 + "\n")

# Keep script running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n\n🛑 Shutting down...")
    ngrok.disconnect(fastapi_tunnel.public_url)
    ngrok.disconnect(flask_tunnel.public_url)
    print("✅ Ngrok tunnels closed")