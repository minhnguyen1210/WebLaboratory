# 🇻🇳 Vietnam Place - Enhanced with HuggingFace AI

Một ứng dụng web hiện đại để khám phá các địa điểm du lịch Việt Nam với tính năng AI mạnh mẽ từ HuggingFace.

## 🎯 Tính năng chính

### 1. 📍 Tìm kiếm địa điểm
- Tìm kiếm địa điểm Việt Nam theo tên
- Hiển thị thông tin thời tiết thời real-time
- Danh sách các điểm du lịch gần đó

### 2. 🗺️ Chỉ dẫn đường
- Tính toán tuyến đường giữa hai địa điểm
- Hướng dẫn chi tiết từng bước
- Hiển thị khoảng cách và thời gian

### 3. 🌐 Dịch văn bản
- Dịch giữa nhiều ngôn ngữ
- Hai phiên bản: Local (Google Translate) + HuggingFace

### 4. 🤖 HuggingFace AI Features (NEW!)
- **Text Generation**: Tạo văn bản từ prompt
- **Summarization**: Tóm tắt các đoạn văn dài
- **Question Answering**: Trả lời câu hỏi dựa trên context
- **Translation**: Dịch văn bản với model Helsinki-NLP

### 5. ☀️ Thông tin thời tiết
- Hiển thị nhiệt độ, độ ẩm, tốc độ gió
- Icon thời tiết tương ứng
- Cập nhật real-time từ OpenWeatherMap

### 6. 👤 Xác thực người dùng
- Đăng ký/Đăng nhập với Firebase
- Lưu dữ liệu địa điểm yêu thích
- Quản lý hồ sơ người dùng

## 🏗️ Kiến trúc hệ thống

```
Frontend (index.html)
    ↓ Gọi API
Flask Backend (main.py)
    ├─ Routes xác thực
    ├─ Routes địa điểm
    ├─ Routes chỉ dẫn đường
    └─ Proxy tới FastAPI
    ↓ Gọi API
FastAPI Backend (huggingface_api.py)
    ├─ Text Generation
    ├─ Summarization
    ├─ Question Answering
    └─ Translation
    ↓ Gọi API
HuggingFace API
    └─ Inference endpoints
```

## 📦 Dependencies

```
Flask==3.0.0
FastAPI==0.104.1
Uvicorn==0.24.0
requests==2.31.0
deep-translator==1.11.4
pydantic==2.5.0
```

## 🚀 Cài đặt & Chạy

### 1. Cài đặt Python dependencies

```powershell
pip install -r requirements.txt
```

### 2. Tạo file `.env`

Copy từ `.env.example`:
```powershell
Copy-Item .env.example .env
```

Điền vào file `.env`:
```
HF_API_TOKEN=hf_YOUR_TOKEN_HERE
FIREBASE_API_KEY=your_firebase_key
```

### 3. Chạy servers

**Option A: Chạy script PowerShell**
```powershell
.\run_servers.ps1
```

**Option B: Chạy riêng lẻ**

Terminal 1 - FastAPI:
```powershell
uvicorn huggingface_api:app --reload --host 0.0.0.0 --port 8000
```

Terminal 2 - Flask:
```powershell
python main.py
```

### 4. Truy cập website
- Website: http://localhost:5000
- FastAPI Docs: http://localhost:8000/docs

## 🌐 Deployment với ngrok/pinggy

### Với ngrok:

```powershell
# Terminal 3: Expose FastAPI
ngrok http 8000

# Cập nhật URL trong main.py
# HF_API_BASE = 'https://your-ngrok-url.ngrok.io'
```

### Với pinggy (không cần đăng ký):

```powershell
ssh -R 80:localhost:8000 -N -T ssh.pinggy.io
```

Xem chi tiết trong file `DEPLOYMENT.md`

## 📝 Sử dụng HuggingFace API

### Từ Frontend (JavaScript)

```javascript
// Text Generation
const result = await hfClient.generateText(
    "Vietnam is...",
    200,  // max_length
    0.7   // temperature
);

// Summarization
const summary = await hfClient.summarizeText(
    "Your long text...",
    150,  // max_length
    50    // min_length
);

// Question Answering
const answer = await hfClient.answerQuestion(
    "What is Vietnam?",
    "Vietnam is a country in Southeast Asia..."
);

// Translation
const translated = await hfClient.translateText(
    "Hello world",
    "en",  // source
    "vi"   // target
);
```

### Từ Flask Backend (Python)

```python
# Gọi tới FastAPI
response = requests.post(
    'http://localhost:8000/api/generate',
    json={'prompt': 'Vietnam...', 'max_length': 100}
)
```

## 🔧 Cấu hình

### Lấy HuggingFace API Token

1. Đăng nhập https://huggingface.co/
2. Settings → Access Tokens
3. Create new token (read access)
4. Copy token vào `.env`

### Models sử dụng

| Tên | Model | Endpoint |
|-----|-------|----------|
| Text Generation | Mistral-7B | `/api/generate` |
| Summarization | BART-large-CNN | `/api/summarize` |
| QA | RoBERTa-base-SQuAD2 | `/api/qa` |
| Translation | Helsinki-NLP | `/api/hf-translate` |

## 🐛 Troubleshooting

### HuggingFace API không kết nối
- Kiểm tra HF_API_TOKEN trong `.env`
- Restart FastAPI backend
- Kiểm tra ngrok URL (nếu deploy)

### CORS Error
- Đã cấu hình CORSMiddleware trong FastAPI
- Kiểm tra browser console cho chi tiết

### Model loading timeout
- Lần đầu tiên load model sẽ chậm (30 giây)
- Lần sau sẽ nhanh hơn

## 📚 Tài liệu

- [Hướng dẫn Deployment](DEPLOYMENT.md)
- [FastAPI Docs](http://localhost:8000/docs)
- [HuggingFace API](https://huggingface.co/docs/inference-api)
- [Flask Docs](https://flask.palletsprojects.com/)

## 🎨 Tính năng giao diện

- **Responsive Design**: Hoạt động tốt trên desktop, tablet, mobile
- **Dark/Light Theme**: Chế độ tối/sáng
- **Real-time Updates**: Dữ liệu cập nhật tức thì
- **Smooth Animations**: Hiệu ứng mượt mà

## 📊 Project Structure

```
.
├── main.py                    # Flask backend chính
├── huggingface_api.py        # FastAPI backend cho HF
├── authentication.py         # Firebase auth
├── geocoding.py             # Nominatim geocoding
├── routing.py               # OSRM routing
├── weather.py               # OpenWeather API
├── translate.py             # Translation functions
├── huggingface_client.js    # HF JavaScript client
├── index.html               # Frontend
├── style.css                # Styling
├── requirements.txt         # Python dependencies
├── .env.example             # Cấu hình mẫu
├── run_servers.ps1          # Script chạy servers
├── DEPLOYMENT.md            # Hướng dẫn deploy
└── README.md                # File này
```

## 🤝 Đóng góp

Để đóng góp, vui lòng:
1. Fork project
2. Tạo branch feature (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

Dự án này được cấp phép dưới MIT License.

## 👨‍💻 Tác giả

Tạo bởi sinh viên VNU-HCMUS

---

**Ghi chú**: Đây là dự án giáo dục. Một số API key được công khai cho mục đích demo. Trong production, vui lòng sử dụng environment variables.
