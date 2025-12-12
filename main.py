from flask import Flask, render_template, request, send_from_directory, jsonify, session
import requests, time, os
from datetime import datetime, UTC
from weather import get_weather
from translate import translate_text, translate_instruction
from geocoding import geocode
from authentication import (
    firebase_signup, firebase_signin, firebase_send_verification_email,
    firebase_send_password_reset, firebase_refresh_token,
    save_user_to_db, get_user_from_db
)
from routing import get_route

current_dir = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=current_dir)

UA = {"User-Agent": "VietnamPlace/1.0 (contact: bsssdd24@gmail.com)"}

# ============ AUTHENTICATION ROUTES ============
@app.route('/api/auth/register', methods=['POST'])
def register():
    """API đăng ký tài khoản mới"""
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        display_name = data.get('display_name', '')
        
        # Đăng ký với Firebase
        result = firebase_signup(email, password, display_name)
        
        if result['success']:
            user_data = result['data']
            
            # Gửi email xác minh
            firebase_send_verification_email(user_data['idToken'])
            
            return jsonify({
                "success": True,
                "message": "Đăng ký thành công! Vui lòng kiểm tra email để xác minh tài khoản.",
                "user": {
                    "email": user_data['email'],
                    "uid": user_data['localId'],
                    "displayName": display_name
                }
            })
        else:
            error_msg = result['error']
            if "EMAIL_EXISTS" in error_msg:
                error_msg = "Email đã được sử dụng"
            elif "WEAK_PASSWORD" in error_msg:
                error_msg = "Mật khẩu quá yếu (tối thiểu 6 ký tự)"
            
            return jsonify({"success": False, "error": error_msg}), 400
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """API đăng nhập"""
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        # Đăng nhập với Firebase
        result = firebase_signin(email, password)
        
        if result['success']:
            user_data = result['data']
            
            # Lấy thông tin từ database
            db_user = get_user_from_db(user_data['localId'], user_data['idToken'])
            
            return jsonify({
                "success": True,
                "message": "Đăng nhập thành công!",
                "user": {
                    "email": user_data['email'],
                    "uid": user_data['localId'],
                    "displayName": db_user.get('displayName', '') if db_user else '',
                    "idToken": user_data['idToken'],
                    "refreshToken": user_data['refreshToken']
                }
            })
        else:
            error_msg = result['error']
            if "INVALID_PASSWORD" in error_msg or "EMAIL_NOT_FOUND" in error_msg or "INVALID_LOGIN_CREDENTIALS" in error_msg:
                error_msg = "Email hoặc mật khẩu không đúng"
            
            return jsonify({"success": False, "error": error_msg}), 401
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """API đăng xuất"""
    return jsonify({"success": True, "message": "Đã đăng xuất"})

@app.route('/api/auth/verify-email', methods=['POST'])
def verify_email():
    """API gửi lại email xác minh"""
    try:
        data = request.json
        id_token = data.get('idToken')
        
        if firebase_send_verification_email(id_token):
            return jsonify({
                "success": True,
                "message": "Email xác minh đã được gửi!"
            })
        else:
            return jsonify({"success": False, "error": "Không thể gửi email"}), 400
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/auth/reset-password', methods=['POST'])
def reset_password():
    """API gửi email đặt lại mật khẩu"""
    try:
        data = request.json
        email = data.get('email')
        
        if firebase_send_password_reset(email):
            return jsonify({
                "success": True,
                "message": "Email đặt lại mật khẩu đã được gửi!"
            })
        else:
            return jsonify({"success": False, "error": "Email không tồn tại"}), 400
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/auth/refresh', methods=['POST'])
def refresh():
    """API làm mới token"""
    try:
        data = request.json
        refresh_token = data.get('refreshToken')
        
        new_token = firebase_refresh_token(refresh_token)
        if new_token:
            return jsonify({
                "success": True,
                "idToken": new_token['id_token'],
                "refreshToken": new_token['refresh_token']
            })
        else:
            return jsonify({"success": False, "error": "Không thể làm mới token"}), 400
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.after_request
def add_ngrok_headers(response):
    """Add headers to bypass ngrok browser warning"""
    response.headers['ngrok-skip-browser-warning'] = 'true'
    return response

@app.route('/style.css')
def style():
    return send_from_directory(current_dir, 'style.css', mimetype='text/css')

@app.route('/huggingface_client.js')
def huggingface_client():
    return send_from_directory(current_dir, 'huggingface_client.js', mimetype='application/javascript')

def find_pois(lat, lon, limit=5):
    radius = 1000 # 1 km
    pois = []
    while len(pois) < limit and radius <= 5000:
        query = f"""
        [out:json][timeout:60];
        (
          node(around:{radius},{lat},{lon})[tourism];
        );
        out center;
        """
        r = requests.post("https://lz4.overpass-api.de/api/interpreter", data=query, headers=UA, timeout=60)
        r.raise_for_status()
        elements = r.json().get("elements", [])
        for el in elements:
            name = el.get("tags", {}).get("name")
            if name and all(p["name"] != name for p in pois):
                poi_weather = get_weather(el["lat"], el["lon"])
                pois.append({
                    "name": name,
                    "lat": el["lat"],
                    "lon": el["lon"],
                    "type": el.get("tags", {}).get("amenity") or el.get("tags", {}).get("tourism"),
                    "weather": poi_weather                
                })
            if len(pois) >= limit:
                break
        radius += 500  
    return pois[:limit]

@app.route("/", methods=["GET", "POST"])
def index():
    pois = []
    lat = lon = None
    display_name = ""
    query = ""
    weather = None

    if request.method == "POST":
        query = request.form.get("location")
        try:
            lat, lon, display_name = geocode(query)
            pois = find_pois(lat, lon, 5)
            weather = get_weather(lat, lon)
        except Exception as e:
            return f"Lỗi: {e}"
    return render_template("index.html", pois=pois, lat=lat, lon=lon,
                           display_name=display_name, query=query, weather=weather)

@app.route("/api/route")
def api_route():
    """API endpoint để lấy tuyến đường"""
    lat1, lon1 = request.args.get("lat1", type=float), request.args.get("lon1", type=float)
    lat2, lon2 = request.args.get("lat2", type=float), request.args.get("lon2", type=float)
    if not all([lat1, lon1, lat2, lon2]):
        return jsonify({"error": "Missing coordinates"}), 400
    route = get_route(lon1, lat1, lon2, lat2)
    if route:
        return jsonify(route)
    return jsonify({"error": "Could not find route"}), 404

@app.route("/api/translate", methods=["POST"])
def api_translate():
    data = request.json
    text = data.get("text")
    target_language = data.get("target", "en")
    translated_text = translate_text(text, target_language)
    return jsonify({
            "translated": translated_text,  
            "original": text,
            "target_lang": target_language
        })

# ============ HUGGINGFACE API PROXY ROUTES ============
# Proxy requests to FastAPI backend
HF_API_BASE = os.environ.get('HF_API_BASE', 'http://localhost:8000')

@app.route("/api/hf/health", methods=["GET"])
def hf_health():
    """Check FastAPI backend health"""
    try:
        response = requests.get(f"{HF_API_BASE}/health", timeout=5)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"success": False, "error": str(e), "status": "offline"}), 503

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint - proxy to FastAPI"""
    try:
        response = requests.get(f"{HF_API_BASE}/health", timeout=5)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"success": False, "error": str(e), "status": "offline"}), 503

@app.route("/api/chat", methods=["POST"])
def api_chat():
    """Proxy chat requests to FastAPI"""
    try:
        response = requests.post(
            f"{HF_API_BASE}/api/chat",
            json=request.get_json(),
            headers={'Content-Type': 'application/json'},
            timeout=60
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 503

@app.route("/api/qa", methods=["POST"])
def api_qa():
    """Proxy QA requests to FastAPI"""
    try:
        response = requests.post(
            f"{HF_API_BASE}/api/qa",
            json=request.get_json(),
            headers={'Content-Type': 'application/json'},
            timeout=60
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 503

# Start FastAPI in background thread when Flask starts
import threading
import subprocess
import time

def start_fastapi_background():
    """Start FastAPI backend in background"""
    print("🚀 Starting FastAPI backend...")
    subprocess.Popen([
        "python", "-m", "uvicorn",
        "huggingface_api:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--workers", "1"
    ])

# Start FastAPI when module loads (for gunicorn)
if os.environ.get('PORT'):  # Running on Render
    fastapi_thread = threading.Thread(target=start_fastapi_background, daemon=True)
    fastapi_thread.start()
    time.sleep(3)  # Wait for FastAPI to start

if __name__ == "__main__":
    # Get port from environment (for Render.com)
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    # Start FastAPI in local development
    if not os.environ.get('PORT'):
        start_fastapi_background()
        time.sleep(3)
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
