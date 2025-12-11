# API Endpoints Documentation

## FastAPI Backend (huggingface_api.py)

Base URL: `http://localhost:8000` (hoặc ngrok/pinggy URL)

### Health & Info

#### GET `/health`
Kiểm tra trạng thái API

**Response (200):**
```json
{
  "status": "online",
  "service": "Vietnam Place HuggingFace Backend"
}
```

#### GET `/api/models`
Lấy danh sách các model có sẵn

**Response (200):**
```json
{
  "models": [
    {
      "name": "text-generation",
      "endpoint": "/api/generate",
      "model": "Mistral-7B-Instruct-v0.1",
      "description": "Tạo văn bản mới dựa trên prompt"
    },
    ...
  ]
}
```

### Text Generation

#### POST `/api/generate`
Tạo văn bản sử dụng Mistral-7B model

**Request:**
```json
{
  "prompt": "Vietnam is a beautiful country",
  "max_length": 100,
  "temperature": 0.7
}
```

**Parameters:**
- `prompt` (string, required): Văn bản khởi đầu
- `max_length` (int, optional): Độ dài tối đa (default: 100)
- `temperature` (float, optional): Độ sáng tạo 0-2 (default: 0.7)

**Response (200):**
```json
{
  "success": true,
  "original": "Vietnam is a beautiful country",
  "generated": "Vietnam is a beautiful country with... [generated text continues]"
}
```

**Error (500/504):**
```json
{
  "detail": "Error message"
}
```

### Summarization

#### POST `/api/summarize`
Tóm tắt văn bản sử dụng BART model

**Request:**
```json
{
  "text": "Long text to summarize...",
  "max_length": 150,
  "min_length": 50
}
```

**Parameters:**
- `text` (string, required): Văn bản cần tóm tắt
- `max_length` (int, optional): Độ dài tối đa tóm tắt (default: 150)
- `min_length` (int, optional): Độ dài tối thiểu (default: 50)

**Response (200):**
```json
{
  "success": true,
  "original": "Long text...",
  "summary": "Summarized text..."
}
```

### Question Answering

#### POST `/api/qa`
Trả lời câu hỏi dựa trên context

**Request:**
```json
{
  "question": "What is Vietnam?",
  "context": "Vietnam is a country in Southeast Asia. It has a rich history..."
}
```

**Parameters:**
- `question` (string, required): Câu hỏi
- `context` (string, required): Đoạn văn chứa đáp án

**Response (200):**
```json
{
  "success": true,
  "question": "What is Vietnam?",
  "answer": "a country in Southeast Asia",
  "score": 0.95
}
```

### Translation

#### POST `/api/hf-translate`
Dịch văn bản giữa các ngôn ngữ

**Request:**
```json
{
  "text": "Hello world",
  "source_lang": "en",
  "target_lang": "vi"
}
```

**Parameters:**
- `text` (string, required): Văn bản cần dịch
- `source_lang` (string, optional): Ngôn ngữ nguồn (default: "en")
- `target_lang` (string, optional): Ngôn ngữ đích (default: "vi")

**Response (200):**
```json
{
  "success": true,
  "original": "Hello world",
  "translated": "Xin chào thế giới",
  "source_lang": "en",
  "target_lang": "vi"
}
```

---

## Flask Backend (main.py)

Base URL: `http://localhost:5000`

### Authentication Routes

#### POST `/api/auth/register`
Đăng ký tài khoản mới

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "display_name": "Nguyễn Văn A"
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "Đăng ký thành công!",
  "user": {
    "email": "user@example.com",
    "uid": "firebaseUID",
    "displayName": "Nguyễn Văn A"
  }
}
```

#### POST `/api/auth/login`
Đăng nhập

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "Đăng nhập thành công!",
  "user": {
    "email": "user@example.com",
    "uid": "firebaseUID",
    "displayName": "Nguyễn Văn A",
    "idToken": "firebaseToken",
    "refreshToken": "refreshToken"
  }
}
```

#### POST `/api/auth/logout`
Đăng xuất

**Response (200):**
```json
{
  "success": true,
  "message": "Đã đăng xuất"
}
```

#### POST `/api/auth/verify-email`
Gửi email xác minh

**Request:**
```json
{
  "idToken": "firebaseToken"
}
```

#### POST `/api/auth/reset-password`
Gửi email đặt lại mật khẩu

**Request:**
```json
{
  "email": "user@example.com"
}
```

### HuggingFace Proxy Routes

#### POST `/api/hf/generate`
Proxy tới FastAPI text generation

**Request:** Same as `/api/generate`

#### POST `/api/hf/summarize`
Proxy tới FastAPI summarization

**Request:** Same as `/api/summarize`

#### POST `/api/hf/qa`
Proxy tới FastAPI QA

**Request:** Same as `/api/qa`

#### POST `/api/hf/translate`
Proxy tới FastAPI translation

**Request:** Same as `/api/hf-translate`

#### GET `/api/hf/models`
Lấy danh sách models

### Location Routes

#### GET `/`
Trang chính (HTML)

#### POST `/`
Tìm kiếm địa điểm

**Form data:**
```
location=Hà Nội
```

**Returns:** HTML page với kết quả

#### GET `/api/route`
Lấy tuyến đường

**Parameters:**
```
lat1=21.0285
lon1=105.8542
lat2=21.1451
lon2=106.6881
```

**Response (200):**
```json
{
  "coordinates": [[21.0285, 105.8542], ...],
  "distance_km": 145.2,
  "duration_min": 150,
  "steps": [
    {
      "instruction": "🚀 Bắt đầu hành trình",
      "distance": 500,
      "duration": 5,
      "name": "Nguyễn Huệ"
    },
    ...
  ]
}
```

#### POST `/api/translate`
Dịch văn bản (sử dụng Google Translate)

**Request:**
```json
{
  "text": "Hello world",
  "target": "vi"
}
```

**Response (200):**
```json
{
  "translated": "Xin chào thế giới",
  "original": "Hello world",
  "target_lang": "vi"
}
```

---

## JavaScript Client (huggingface_client.js)

```javascript
// Khởi tạo
let hfClient = new HuggingFaceClient('http://localhost:8000');

// Kiểm tra kết nối
hfClient.checkConnection();

// Text generation
const result = await hfClient.generateText(prompt, maxLength, temperature);

// Summarization
const summary = await hfClient.summarizeText(text, maxLength, minLength);

// Question answering
const answer = await hfClient.answerQuestion(question, context);

// Translation
const translated = await hfClient.translateText(text, sourceLang, targetLang);

// Get models
const models = await hfClient.getAvailableModels();
```

---

## Error Handling

### HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | OK | Successful request |
| 400 | Bad Request | Missing required parameters |
| 401 | Unauthorized | Invalid credentials |
| 404 | Not Found | Endpoint không tồn tại |
| 500 | Server Error | Processing error |
| 504 | Gateway Timeout | HuggingFace API timeout |

### Error Response Format

```json
{
  "detail": "Error message here"
}
```

hoặc

```json
{
  "success": false,
  "error": "Error message here"
}
```

---

## Rate Limiting

- **ngrok free tier**: 40 requests/phút
- **HuggingFace**: Variable theo model
- **Firebase**: 1 million reads/day (free)

---

## Testing with curl

### Text Generation
```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Vietnam","max_length":100,"temperature":0.7}'
```

### Summarization
```bash
curl -X POST http://localhost:8000/api/summarize \
  -H "Content-Type: application/json" \
  -d '{"text":"Your long text here","max_length":150}'
```

### Question Answering
```bash
curl -X POST http://localhost:8000/api/qa \
  -H "Content-Type: application/json" \
  -d '{"question":"What is Vietnam?","context":"Vietnam is..."}'
```

### Translation
```bash
curl -X POST http://localhost:8000/api/hf-translate \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello world","source_lang":"en","target_lang":"vi"}'
```

---

## Documentation Tools

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

