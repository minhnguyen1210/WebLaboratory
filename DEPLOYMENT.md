# 🚀 Vietnam Place - Hướng dẫn Deployment

## Architecture

```
Frontend (index.html) 
    ↓ calls
Flask Backend (main.py) 
    ↓ calls
FastAPI Backend (huggingface_api.py)
    ↓ calls
HuggingFace API
```

## 📋 Chuẩn bị

### 1. Cài đặt Dependencies

```powershell
pip install -r requirements.txt
```

### 2. Tạo file `.env`

Copy từ `.env.example` và điền thông tin:

```
FIREBASE_API_KEY=your_key
HF_API_TOKEN=hf_your_token_from_huggingface
HF_API_BASE=http://localhost:8000
```

**Nhận HuggingFace Token:**
1. Đăng nhập tại https://huggingface.co/
2. Vào Settings → Access Tokens
3. Create new token (read access là đủ)
4. Copy token vào `.env` file

---

## 🏃 Chạy Local (Development)

### Terminal 1: Chạy FastAPI Backend

```powershell
uvicorn huggingface_api:app --reload --host 0.0.0.0 --port 8000
```

**Output sẽ hiển thị:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Press CTRL+C to quit
```

**API Documentation:** http://localhost:8000/docs

### Terminal 2: Chạy Flask Backend

```powershell
python main.py
```

**Output sẽ hiển thị:**
```
Running on http://127.0.0.1:5000
```

### Truy cập Website
- Mở browser: http://localhost:5000

---

## 🌐 Deploy với ngrok

### 1. Cài đặt ngrok

**Tải từ:** https://ngrok.com/download

```powershell
# Extract ngrok
# Thêm ngrok vào PATH hoặc chạy từ thư mục

# Xác thực ngrok (cần tài khoản free)
ngrok authtoken YOUR_AUTHTOKEN
```

### 2. Expose FastAPI Backend với ngrok

Trong Terminal 1 đang chạy FastAPI:

```powershell
ngrok http 8000
```

**Output sẽ hiển thị:**
```
ngrok by @inconshrevable (Ctrl+C to quit)

Session Status    online
Account           your_email@gmail.com
Version           3.0.0
Region            us (United States)
Forwarding        https://1234-56-789-012-34.ngrok.io -> http://localhost:8000
```

**Sao chép URL:** `https://1234-56-789-012-34.ngrok.io`

### 3. Cập nhật Flask Backend

Trong file `main.py` hoặc file `.env`:

```python
HF_API_BASE = os.environ.get('HF_API_BASE', 'https://1234-56-789-012-34.ngrok.io')
```

### 4. Expose Flask Backend (Optional)

Nếu muốn expose website qua ngrok:

```powershell
ngrok http 5000
```

---

## 🔌 Deploy với Pinggy (Không cần đăng ký)

### 1. Expose FastAPI Backend

```powershell
ssh -R 80:localhost:8000 -N -T ssh.pinggy.io
```

**Output sẽ hiển thị:**
```
Forwarding: https://randomstring.pinggy.io → http://localhost:8000
```

### 2. Cập nhật URL

```python
HF_API_BASE = 'https://randomstring.pinggy.io'
```

---

## ✅ Kiểm tra Kết nối

### 1. Kiểm tra FastAPI Backend

```powershell
# Local
curl http://localhost:8000/health

# Via ngrok
curl https://your-ngrok-url.ngrok.io/health

# Via pinggy
curl https://your-pinggy-url.pinggy.io/health
```

**Response:**
```json
{
  "status": "online",
  "service": "Vietnam Place HuggingFace Backend"
}
```

### 2. Kiểm tra Flask Backend

```powershell
curl http://localhost:5000/api/hf/models
```

---

## 🎯 Sử dụng HuggingFace API từ Frontend

### Ví dụ 1: Text Generation

```javascript
const result = await hfClient.generateText(
    "Vietnam is a beautiful country",
    200,  // max_length
    0.7   // temperature
);
console.log(result.generated);
```

### Ví dụ 2: Summarization

```javascript
const summary = await hfClient.summarizeText(
    "Your long text here...",
    150,  // max_length
    50    // min_length
);
console.log(summary.summary);
```

### Ví dụ 3: Question Answering

```javascript
const answer = await hfClient.answerQuestion(
    "What is Vietnam?",
    "Vietnam is a country in Southeast Asia..."
);
console.log(answer.answer);
```

### Ví dụ 4: Translation

```javascript
const translation = await hfClient.translateText(
    "Hello world",
    "en",  // source language
    "vi"   // target language
);
console.log(translation.translated);
```

---

## 🐛 Troubleshooting

### 1. Error: "Failed to connect to HuggingFace API"

**Nguyên nhân:** URL không đúng hoặc ngrok session đã hết

**Giải pháp:**
```powershell
# Kiểm tra ngrok đang chạy
ngrok http 8000

# Cập nhật URL mới
```

### 2. Error: "401 Unauthorized"

**Nguyên nhân:** HuggingFace API token sai

**Giải pháp:**
```
1. Kiểm tra token trong .env file
2. Lấy token mới từ https://huggingface.co/settings/tokens
3. Restart FastAPI backend
```

### 3. Error: "503 Service Unavailable"

**Nguyên nhân:** Model đang load từ HuggingFace

**Giải pháp:** Chờ vài giây rồi thử lại (lần đầu tiên sẽ chậm)

### 4. CORS Error

**Nguyên nhân:** Frontend gọi tới FastAPI có CORS issue

**Giải pháp:** Đã cấu hình trong `huggingface_api.py` với `CORSMiddleware`

---

## 📊 API Endpoints

### FastAPI Backend (huggingface_api.py)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Kiểm tra trạng thái |
| `/api/models` | GET | Danh sách models |
| `/api/generate` | POST | Text Generation |
| `/api/summarize` | POST | Summarization |
| `/api/qa` | POST | Question Answering |
| `/api/hf-translate` | POST | Translation |

### Flask Backend (main.py)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/hf/generate` | POST | Proxy to FastAPI |
| `/api/hf/summarize` | POST | Proxy to FastAPI |
| `/api/hf/qa` | POST | Proxy to FastAPI |
| `/api/hf/translate` | POST | Proxy to FastAPI |
| `/api/hf/models` | GET | Get models list |

---

## 🚀 Production Tips

1. **Sử dụng environment variables cho tất cả sensitive data**

2. **Implement caching để tránh call API quá nhiều**

3. **Rate limiting để tránh abuse**

4. **Sử dụng HTTPS (ngrok/pinggy tự cung cấp)**

5. **Monitor API usage** từ HuggingFace dashboard

6. **Setup error handling & logging**

---

## 📝 Notes

- ngrok free tier có 40 request/phút limit
- Pinggy không có limit nhưng URL thay đổi mỗi lần kết nối
- HuggingFace models có rate limit, nên không nên spam requests
- Lần đầu load model sẽ chậm (có thể mất 30 giây)

---

## 🔗 Tài liệu Liên quan

- https://ngrok.com/
- https://pinggy.io/
- https://huggingface.co/docs/inference-api
- https://fastapi.tiangolo.com/
- https://flask.palletsprojects.com/

