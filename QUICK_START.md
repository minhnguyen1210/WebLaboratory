# ⚡ Quick Start Guide - Vietnam Place

Bắt đầu nhanh trong 5 phút!

## 🎯 Bước 1: Chuẩn bị (1 phút)

### A. Lấy HuggingFace Token
1. Truy cập https://huggingface.co/settings/tokens
2. Click "New token"
3. Chọn "Read" access
4. Copy token

### B. Tạo file `.env`
```powershell
Copy-Item .env.example .env
```

Mở `.env` và thêm:
```
HF_API_TOKEN=hf_PASTE_YOUR_TOKEN_HERE
```

## 🚀 Bước 2: Chạy Servers (2 phút)

### Option A: PowerShell Script (Recommended)
```powershell
.\run_servers.ps1
```

### Option B: Batch File
```powershell
.\startup.bat
```

### Option C: Manual
Terminal 1:
```powershell
uvicorn huggingface_api:app --reload --host 0.0.0.0 --port 8000
```

Terminal 2:
```powershell
python main.py
```

## 🌐 Bước 3: Truy cập Website (1 phút)

Mở browser:
- **Website**: http://localhost:5000
- **FastAPI Docs**: http://localhost:8000/docs

## ✅ Kiểm tra hoạt động

### Test fastAPI
```powershell
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "online",
  "service": "Vietnam Place HuggingFace Backend"
}
```

### Test Website
1. Mở http://localhost:5000
2. Tìm kiếm địa điểm: "Hà Nội" hoặc "Hội An"
3. Thử các features trong HuggingFace AI tab

## 🌐 Expose với ngrok (1 phút - Optional)

### Cài ngrok
```powershell
# Tải từ https://ngrok.com/download
# Hoặc dùng winget
winget install ngrok
```

### Expose FastAPI
```powershell
ngrok http 8000
```

**Copy URL**: `https://xxxxxxxx-xxxx.ngrok.io`

### Cập nhật URL
Trong `main.py`, tìm dòng:
```python
HF_API_BASE = os.environ.get('HF_API_BASE', 'http://localhost:8000')
```

Thay bằng:
```python
HF_API_BASE = 'https://xxxxxxxx-xxxx.ngrok.io'
```

Hoặc cập nhật `.env`:
```
HF_API_BASE=https://xxxxxxxx-xxxx.ngrok.io
```

## 🎮 Sử dụng Features

### 1. Tìm kiếm địa điểm
- Nhập địa chỉ: "Hà Nội", "Hạ Long", "Sapa"
- Xem bản đồ, thời tiết, điểm du lịch gần đó

### 2. Chỉ dẫn đường
- Click vào một điểm du lịch
- Xem tuyến đường chi tiết từng bước

### 3. HuggingFace AI Features
- **Summarize**: Tóm tắt bài viết dài
- **Generate**: Tạo văn bản từ prompt
- **QA**: Hỏi đáp
- **Translate**: Dịch với HuggingFace

## ⚙️ Cấu hình nâng cao

Xem file `DEPLOYMENT.md` để:
- Cấu hình CORS
- Bảo mật API
- Deploy trên cloud
- Caching strategies
- Rate limiting

## 🆘 Troubleshooting

### Error: "Python not found"
```powershell
# Kiểm tra Python
python --version

# Nếu không có, cài đặt từ python.org
```

### Error: "Module not found"
```powershell
# Cài lại dependencies
pip install -r requirements.txt
```

### Error: "HuggingFace API timeout"
- Lần đầu load model sẽ chậm (30 giây)
- Token không chính xác
- Kiểm tra token trong https://huggingface.co/settings/tokens

### Error: "CORS error"
- Kiểm tra URL FastAPI
- Kiểm tra cấu hình CORSMiddleware

### Servers không start
- Port đang bị dùng
- Đóng terminal cũ
- Chạy: `netstat -ano | findstr :8000` để kiểm tra

## 📚 Tài liệu thêm

- [README.md](README.md) - Tổng quan đầy đủ
- [DEPLOYMENT.md](DEPLOYMENT.md) - Hướng dẫn deploy chi tiết
- [FastAPI Docs](http://localhost:8000/docs) - API documentation

## 🎓 Học thêm

### HuggingFace Models
```
- Mistral-7B: Text generation
- BART: Summarization
- RoBERTa: Question answering
- Helsinki-NLP: Translation
```

Xem tại: https://huggingface.co/models

### Endpoints có sẵn
```
GET  /health                 - Health check
GET  /api/models             - List available models
POST /api/generate           - Text generation
POST /api/summarize          - Text summarization
POST /api/qa                 - Question answering
POST /api/hf-translate       - Translation
```

## 💡 Tips

1. **Để lại FastAPI chạy lâu**: Cửa sổ terminal sẽ in log
2. **Xem API docs**: http://localhost:8000/docs (Swagger UI)
3. **Test API**: Dùng Postman hoặc curl
4. **Lưu token an toàn**: Đừng commit `.env` lên git

---

**Hết! Website của bạn đã sẵn sàng.** 🎉

Câu hỏi? Xem README.md hoặc DEPLOYMENT.md
