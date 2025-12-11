# 🏗️ KIẾN TRÚC HỆ THỐNG - Vietnam Place Chatbot

## 📊 Flow Chart

```
User Browser (index.html)
    ↓
    ├─→ huggingface_client.js (JS Client)
    │       ↓
    │   Flask Server (main.py) :5000
    │       ↓ (proxy)
    │   FastAPI Backend (huggingface_api.py) :8000
    │       ↓
    │   HuggingFace API (router.huggingface.co)
    │       ↓
    │   Mistral-7B-Instruct Model
    │
    └─→ Leaflet Maps, Weather, Geocoding, etc.
```

## 🔗 Endpoint Mapping

### Frontend → FastAPI (qua Flask proxy)
```
huggingface_client.js          FastAPI                    HuggingFace
────────────────────────────────────────────────────────────────────
hfClient.chat(message)    →   /api/chat              →   Mistral-7B-Instruct
hfClient.askQuestion()    →   /api/qa                →   RoBERTa-SQuAD2
hfClient.checkConnection()→   /health                    (local check)
```

### Flask Routes
```
Route                          Purpose
─────────────────────────────────────────────────────
/                              Main page (index.html)
/style.css                     Serve CSS
/huggingface_client.js         Serve JS client
/api/auth/*                    Authentication (Firebase)
/api/route                     Get directions (OSRM)
/api/translate                 Translate text
/api/hf/health                 Check FastAPI status
```

### FastAPI Endpoints
```
Endpoint                       Model                     Purpose
──────────────────────────────────────────────────────────────────────
POST /api/chat                 Mistral-7B-Instruct       Conversational AI
POST /api/qa                   RoBERTa-SQuAD2            Question Answering
GET  /health                   -                         Health check
```

## 📁 File Responsibilities

### 1. **index.html** (Frontend UI)
- Hiển thị giao diện chatbot
- Gọi `hfClient.chat()` khi user gửi tin nhắn
- Hiển thị lịch sử hội thoại
- Functions: `askChatbotAI()`, `clearChatbotAI()`

### 2. **huggingface_client.js** (JS Client)
- Class `HuggingFaceQAClient`
- Method `chat(message)` → gọi `/api/chat`
- Method `askQuestion(q, ctx)` → gọi `/api/qa`
- Quản lý `conversationHistory[]`
- Tự động check connection khi load

### 3. **main.py** (Flask Server)
- Serve static files (HTML, CSS, JS)
- Authentication routes (Firebase)
- Map/weather/routing routes
- Health check proxy: `/api/hf/health`

### 4. **huggingface_api.py** (FastAPI Backend)
- **POST /api/chat**: Chat với Mistral-7B
  - Input: `{message, conversation_history, model}`
  - Output: `{success, response, model}`
- **POST /api/qa**: QA với RoBERTa
  - Input: `{question, context}`
  - Output: `{success, answer, score}`

## 🤖 Models Used

### Primary: Mistral-7B-Instruct-v0.2
- **Endpoint**: `/api/chat`
- **Purpose**: Conversational AI (chatbot chính)
- **URL**: `router.huggingface.co/v1/chat/completions`
- **Strengths**: Hội thoại tự nhiên, hiểu context tốt

### Backup: RoBERTa-base-SQuAD2
- **Endpoint**: `/api/qa`
- **Purpose**: Question Answering (backward compatibility)
- **URL**: `router.huggingface.co/models/deepset/roberta-base-squad2`
- **Strengths**: Trả lời câu hỏi ngắn dựa trên context

## 🔄 Conversation Flow

```
1. User nhập: "Gợi ý địa điểm du lịch ở Đà Nẵng"
   ↓
2. askChatbotAI() được gọi
   ↓
3. hfClient.chat(message)
   ↓
4. POST http://localhost:8000/api/chat
   Body: {
     message: "Gợi ý địa điểm...",
     conversation_history: [
       {role: "user", content: "..."},
       {role: "assistant", content: "..."}
     ],
     model: "default"
   }
   ↓
5. FastAPI → HuggingFace Router API
   ↓
6. Response: {
     success: true,
     response: "Đà Nẵng có nhiều địa điểm đẹp...",
     model: "mistralai/Mistral-7B-Instruct-v0.2"
   }
   ↓
7. JS client lưu vào conversationHistory
   ↓
8. UI hiển thị message
```

## ⚙️ Configuration

### Environment Variables
```bash
HF_API_TOKEN=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
HF_API_BASE=http://localhost:8000  # Flask → FastAPI
```

### Ports
- **Flask**: 5000 (User-facing)
- **FastAPI**: 8000 (Internal API)

## 🚀 Startup Sequence

```bash
# Terminal 1: Start FastAPI
cd "C:\Users\Admin\OneDrive - VNU-HCMUS\Desktop\24127078"
python -m uvicorn huggingface_api:app --host 0.0.0.0 --port 8000

# Terminal 2: Start Flask
cd "C:\Users\Admin\OneDrive - VNU-HCMUS\Desktop\24127078"
python main.py

# Browser
http://localhost:5000
```

## ✅ Đã Fix

### 1. Xóa Duplicate Routes
- ❌ `main.py` có `/api/hf/chat` gọi trực tiếp HF
- ✅ Đã xóa, chỉ giữ proxy `/api/hf/health`

### 2. JS Client Endpoint
- ❌ `chat()` gọi `/api/qa` (sai model)
- ✅ Sửa thành gọi `/api/chat` (đúng model)

### 3. Response Format
- ❌ JS expect `data.answer` (từ QA)
- ✅ Sửa thành `data.response` (từ Chat)

### 4. Conversation History
- ✅ Đồng bộ giữa JS client và FastAPI
- ✅ Format: `[{role, content}, ...]`

## 🎯 Features Available

### Chatbot AI ✅
- Hội thoại tự nhiên với Mistral-7B
- Nhớ context từ lịch sử (20 tin nhắn gần nhất)
- Trả lời về du lịch Việt Nam

### Place Search ✅
- Tìm địa điểm du lịch
- Hiển thị bản đồ Leaflet
- Thông tin thời tiết

### Navigation ✅
- Chỉ đường OSRM
- Tính khoảng cách và thời gian

### Translation ✅
- Dịch văn bản đa ngôn ngữ

### Authentication ✅
- Đăng ký/đăng nhập Firebase

## 🐛 Debugging

```javascript
// Check API status
hfClient.checkConnection()
console.log(hfClient.isOnline) // true/false
console.log(hfClient.conversationHistory) // Xem lịch sử

// Test chat
await hfClient.chat("xin chào")

// Clear history
hfClient.clearHistory()
```

## 📝 Notes

- **Token Limit**: HuggingFace API có giới hạn rate (503 nếu model đang load)
- **History Limit**: Tự động giữ 20 messages cuối (10 cặp Q&A)
- **Fallback**: Nếu `/api/chat` fail, có thể dùng `/api/qa` (kém hơn)
