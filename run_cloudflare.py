"""
Script tự động chạy FastAPI + Flask với Cloudflare Tunnel
Hoàn toàn MIỄN PHÍ - KHÔNG CÓ WARNING PAGE!
Chạy: python run_cloudflare.py

Yêu cầu: cài cloudflared
Cài đặt: winget install cloudflare.cloudflared
"""

import os
import time
import subprocess
import threading
import signal
import sys
import re

print("🚀 Starting Vietnam Place with Cloudflare Tunnel...\n")

# ============ GLOBAL VARIABLES ============
fastapi_process = None
flask_process = None
cloudflare_process = None
cloudflare_url = None

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

def start_cloudflare():
    """Chạy Cloudflare tunnel cho Flask"""
    global cloudflare_process, cloudflare_url
    print("\n🌐 Starting Cloudflare Tunnel (port 5000)...")
    
    # Kiểm tra cloudflared đã cài chưa
    try:
        subprocess.run(["cloudflared", "--version"], 
                      capture_output=True, check=True)
    except:
        print("❌ cloudflared chưa được cài đặt!")
        print("\n📝 Cài đặt cloudflared:")
        print("   winget install cloudflare.cloudflared")
        print("\nSau khi cài xong, chạy lại script này")
        return None
    
    # Chạy Cloudflare tunnel
    cloudflare_process = subprocess.Popen(
        ["cloudflared", "tunnel", "--url", "http://localhost:5000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    # Đọc output để lấy URL
    print("⏳ Waiting for Cloudflare URL...")
    timeout = time.time() + 45
    
    while time.time() < timeout:
        try:
            line = cloudflare_process.stdout.readline()
            if not line:
                if cloudflare_process.poll() is not None:
                    print("❌ Cloudflare process exited")
                    return None
                time.sleep(0.1)
                continue
            
            line = line.strip()
            if line:
                # In tất cả output để debug
                if any(keyword in line.lower() for keyword in ['https://', 'trycloudflare.com', 'your url']):
                    print(f"   {line}")
                
                # Tìm URL (https://xxxxx.trycloudflare.com)
                match = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
                if match:
                    cloudflare_url = match.group(0)
                    print(f"\n✅ Cloudflare URL found: {cloudflare_url}")
                    return cloudflare_url
                        
        except Exception as e:
            print(f"   Error: {e}")
            continue
    
    print("❌ Timeout waiting for Cloudflare URL")
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
    
    global fastapi_process, flask_process, cloudflare_process
    
    if cloudflare_process:
        print("   Closing Cloudflare tunnel...")
        cloudflare_process.terminate()
        try:
            cloudflare_process.wait(timeout=5)
        except:
            cloudflare_process.kill()
    
    if fastapi_process:
        print("   Stopping FastAPI...")
        fastapi_process.terminate()
        try:
            fastapi_process.wait(timeout=5)
        except:
            fastapi_process.kill()
    
    if flask_process:
        print("   Stopping Flask...")
        flask_process.terminate()
        try:
            flask_process.wait(timeout=5)
        except:
            flask_process.kill()
    
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
    
    # Step 2: Start Cloudflare và lấy URL
    url = start_cloudflare()
    
    if not url:
        print("\n❌ Không lấy được Cloudflare URL!")
        print("💡 Hãy chắc chắn đã cài: winget install cloudflare.cloudflared")
        cleanup()
    
    # Step 3: Cập nhật JavaScript với URL
    if not update_client_js(url):
        print("⚠️ Warning: Could not update JavaScript file")
    
    # Step 4: Start Flask
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
    print("⚡ 100% FREE - No limits")
    print("⚡ Unlimited bandwidth")
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
        if cloudflare_process and cloudflare_process.poll() is not None:
            print("❌ Cloudflare tunnel closed!")
            break
            
except KeyboardInterrupt:
    cleanup()
except Exception as e:
    print(f"\n❌ Error: {e}")
    cleanup()
