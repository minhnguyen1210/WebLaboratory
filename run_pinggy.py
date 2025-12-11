"""
Script tự động chạy FastAPI + Flask với Pinggy (Không có warning page!)
Chạy: python run_pinggy.py

Cần Pinggy Token trong file .env:
PINGGY_TOKEN=your_token_here

Lấy token miễn phí tại: https://dashboard.pinggy.io
"""

import os
import re
import time
import subprocess
import threading
import signal
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("🚀 Starting Vietnam Place with Pinggy...\n")

# ============ GLOBAL VARIABLES ============
fastapi_process = None
flask_process = None
pinggy_process = None
pinggy_url = None

# ============ FUNCTIONS ============

def start_fastapi():
    """Chạy FastAPI backend"""
    global fastapi_process
    print("📦 Starting FastAPI backend (port 8000)...")
    fastapi_process = subprocess.Popen([
        "python", "-m", "uvicorn", 
        "huggingface_api:app", 
        "--host", "0.0.0.0", 
        "--port", "8000"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

def start_flask():
    """Chạy Flask frontend"""
    global flask_process
    print("📦 Starting Flask frontend (port 5000)...")
    flask_process = subprocess.Popen(
        ["python", "main.py"],
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        text=True
    )

def start_pinggy():
    """Chạy Pinggy tunnel cho Flask với token"""
    global pinggy_process, pinggy_url
    
    # Lấy token từ .env
    token = os.getenv('PINGGY_TOKEN')
    
    if not token:
        print("\n❌ Thiếu PINGGY_TOKEN trong file .env!")
        print("\n📝 Hướng dẫn lấy token (FREE):")
        print("   1. Truy cập: https://dashboard.pinggy.io")
        print("   2. Đăng ký/Đăng nhập")
        print("   3. Copy token từ dashboard")
        print("   4. Thêm vào file .env: PINGGY_TOKEN=your_token_here")
        print("\n💡 Hoặc dùng ngrok (đã có token): python run.py")
        return None
    
    print("\n🌐 Starting Pinggy tunnel with token...")
    
    # Chạy Pinggy với token - password sẽ là token
    cmd = f"ssh -p 443 -R0:localhost:5000 -o StrictHostKeyChecking=no {token}@a.pinggy.io"
    
    pinggy_process = subprocess.Popen(
        cmd,
        shell=True,
        stdin=subprocess.PIPE,  # Cho phép gửi input
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding='utf-8',
        errors='ignore',
        bufsize=0  # Unbuffered
    )
    
    # Gửi token làm password
    try:
        print("⏳ Sending password...")
        pinggy_process.stdin.write(token + '\n')
        pinggy_process.stdin.flush()
    except:
        pass
    
    # Đọc output để lấy URL
    print("⏳ Waiting for Pinggy URL...")
    timeout = time.time() + 45
    
    while time.time() < timeout:
        try:
            line = pinggy_process.stdout.readline()
            if not line:
                if pinggy_process.poll() is not None:
                    print("❌ Pinggy process exited")
                    return None
                time.sleep(0.1)
                continue
            
            line = line.strip()
            if line:
                # Chỉ in dòng quan trọng
                if any(keyword in line.lower() for keyword in ['http', 'tunnel', 'pinggy', 'forwarding']):
                    print(f"   {line}")
                
                # Tìm URL Pinggy (hỗ trợ mọi subdomain: .a.free.pinggy.link, .pinggy.io, etc)
                match = re.search(r'https://[a-zA-Z0-9-]+\.[a-z.]*pinggy\.(link|io|online)', line)
                if match:
                    url = match.group(0)
                    # Bỏ qua dashboard.pinggy.io
                    if 'dashboard' not in url:
                        pinggy_url = url
                        print(f"\n✅ Pinggy URL found: {pinggy_url}")
                        return pinggy_url
                        
        except Exception as e:
            print(f"   Error: {e}")
            continue
    
    print("❌ Timeout waiting for Pinggy URL")
    return None

def update_client_js(url):
    """Cập nhật huggingface_client.js với URL mới"""
    print(f"\n📝 Updating huggingface_client.js with: {url}")
    
    try:
        with open('huggingface_client.js', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Tìm và thay thế URL trong constructor
        pattern = r"constructor\(apiBase = '[^']+'\)"
        new_constructor = f"constructor(apiBase = '{url}')"
        content = re.sub(pattern, new_constructor, content)
        
        with open('huggingface_client.js', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ huggingface_client.js updated successfully")
        return True
    except Exception as e:
        print(f"❌ Error updating file: {e}")
        return False

def cleanup(signum=None, frame=None):
    """Dọn dẹp khi tắt script"""
    print("\n\n🛑 Shutting down all services...")
    
    global fastapi_process, flask_process, pinggy_process
    
    if pinggy_process:
        print("   Closing Pinggy tunnel...")
        pinggy_process.terminate()
        pinggy_process.wait(timeout=5)
    
    if fastapi_process:
        print("   Stopping FastAPI...")
        fastapi_process.terminate()
        fastapi_process.wait(timeout=5)
    
    if flask_process:
        print("   Stopping Flask...")
        flask_process.terminate()
        flask_process.wait(timeout=5)
    
    print("✅ All services stopped")
    sys.exit(0)

# Register signal handlers
signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

# ============ START SERVERS ============

try:
    # Step 1: Start FastAPI
    fastapi_thread = threading.Thread(target=start_fastapi, daemon=True)
    fastapi_thread.start()
    print("✅ FastAPI thread started")
    time.sleep(5)  # Đợi FastAPI khởi động
    
    # Step 2: Start Pinggy và lấy URL
    url = start_pinggy()
    
    if not url:
        print("\n❌ Không lấy được Pinggy URL!")
        print("💡 Nếu chưa có token, dùng ngrok thay thế: python run.py")
        cleanup()
    
    # Step 3: JavaScript sẽ gọi CÙNG domain (Pinggy URL)
    # Flask sẽ proxy requests đến FastAPI localhost:8000
    # Không cần update URL vì frontend và backend đều qua Pinggy
    print("\n📝 Note: Frontend và API đều dùng chung Pinggy URL")
    print("   Frontend: " + url)
    print("   API: " + url + "/api/*")
    
    # Step 4: Update JavaScript để dùng relative path
    if not update_client_js(''):  # Empty string = same domain
        print("⚠️ Warning: Could not update JavaScript file")
    
    # Step 5: Start Flask
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()
    print("\n✅ Flask thread started")
    time.sleep(3)
    
    # ============ SUMMARY ============
    
    print("\n" + "="*60)
    print("🎉 ALL SERVICES READY!")
    print("="*60)
    print(f"🌐 Your Website:     {url}")
    print(f"📊 FastAPI Backend:  http://localhost:8000")
    print(f"🖥️  Flask Frontend:   http://localhost:5000")
    print("="*60)
    print("\n💡 Share this URL with your friends:")
    print(f"   👉 {url}")
    print("\n⚡ NO WARNING PAGE - Direct access!")
    print("⏰ Session Duration: 60 minutes (free tier)")
    print("\n⏸️  Press Ctrl+C to stop all services")
    print("="*60 + "\n")
    
    # Keep script running
    while True:
        time.sleep(1)
        
        # Check if processes are still alive
        if fastapi_process and fastapi_process.poll() is not None:
            print("❌ FastAPI crashed!")
            break
        if flask_process and flask_process.poll() is not None:
            print("❌ Flask crashed!")
            break
        if pinggy_process and pinggy_process.poll() is not None:
            print("❌ Pinggy tunnel closed!")
            break
            
except KeyboardInterrupt:
    cleanup()
except Exception as e:
    print(f"\n❌ Error: {e}")
    cleanup()
