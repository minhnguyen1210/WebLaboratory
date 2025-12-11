import requests, os
from flask import Flask, request, jsonify
import time
from datetime import datetime, UTC

# FIREBASE 
FIREBASE_API_KEY = os.environ.get('FIREBASE_API_KEY', "AIzaSyBORzW2hqQe73zbpxBPIKiYbTmdfbvTXBw")
FIREBASE_AUTH_DOMAIN = "tesst-3a3fb.firebaseapp.com"
FIREBASE_DATABASE_URL = "https://tesst-3a3fb-default-rtdb.firebaseio.com"
FIREBASE_PROJECT_ID = "tesst-3a3fb"

# Firebase REST API Endpoints
FIREBASE_AUTH_BASE = "https://identitytoolkit.googleapis.com/v1/accounts"
FIREBASE_DB_BASE = FIREBASE_DATABASE_URL

def firebase_signup(email, password, display_name=""):
    """Đăng ký user mới với Firebase REST API"""
    url = f"{FIREBASE_AUTH_BASE}:signUp?key={FIREBASE_API_KEY}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        
        # Cập nhật display name nếu có
        if display_name:
            update_url = f"{FIREBASE_AUTH_BASE}:update?key={FIREBASE_API_KEY}"
            update_payload = {
                "idToken": data['idToken'],
                "displayName": display_name,
                "returnSecureToken": True
            }
            requests.post(update_url, json=update_payload)
        
        # Lưu thông tin user vào database
        user_data = {
            "email": email,
            "displayName": display_name,
            "createdAt": datetime.now(UTC).isoformat(),
            "emailVerified": False
        }
        save_user_to_db(data['localId'], user_data, data['idToken'])
        
        return {"success": True, "data": data}
    else:
        error = response.json()
        return {"success": False, "error": error.get('error', {}).get('message', 'Unknown error')}

def firebase_signin(email, password):
    """Đăng nhập với Firebase REST API"""
    url = f"{FIREBASE_AUTH_BASE}:signInWithPassword?key={FIREBASE_API_KEY}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return {"success": True, "data": response.json()}
    else:
        error = response.json()
        return {"success": False, "error": error.get('error', {}).get('message', 'Unknown error')}

def firebase_send_verification_email(id_token):
    """Gửi email xác minh"""
    url = f"{FIREBASE_AUTH_BASE}:sendOobCode?key={FIREBASE_API_KEY}"
    payload = {
        "requestType": "VERIFY_EMAIL",
        "idToken": id_token
    }
    
    response = requests.post(url, json=payload)
    return response.status_code == 200

def firebase_send_password_reset(email):
    """Gửi email đặt lại mật khẩu"""
    url = f"{FIREBASE_AUTH_BASE}:sendOobCode?key={FIREBASE_API_KEY}"
    payload = {
        "requestType": "PASSWORD_RESET",
        "email": email
    }
    
    response = requests.post(url, json=payload)
    return response.status_code == 200

def firebase_get_user_data(id_token):
    """Lấy thông tin user từ Firebase"""
    url = f"{FIREBASE_AUTH_BASE}:lookup?key={FIREBASE_API_KEY}"
    payload = {"idToken": id_token}
    
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        users = response.json().get('users', [])
        return users[0] if users else None
    return None

def firebase_refresh_token(refresh_token):
    """Làm mới token"""
    url = f"https://securetoken.googleapis.com/v1/token?key={FIREBASE_API_KEY}"
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }
    
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()
    return None

def save_user_to_db(user_id, user_data, id_token):
    """Lưu thông tin user vào Realtime Database"""
    url = f"{FIREBASE_DB_BASE}/users/{user_id}.json?auth={id_token}"
    response = requests.put(url, json=user_data)
    return response.status_code == 200

def get_user_from_db(user_id, id_token):
    """Lấy thông tin user từ Realtime Database"""
    url = f"{FIREBASE_DB_BASE}/users/{user_id}.json?auth={id_token}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None
