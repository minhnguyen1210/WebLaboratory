"""
FastAPI backend - Chatbot using HuggingFace Conversational AI
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
from typing import List, Optional

# Khởi tạo FastAPI
app = FastAPI(title="Vietnam Place - Chatbot AI", version="2.0")

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Token
HF_API_TOKEN = os.environ.get('HF_API_TOKEN', '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')

# HuggingFace Conversational Models
# Sử dụng model chat mạnh và miễn phí
CHAT_MODELS = {
    "default": "mistralai/Mistral-7B-Instruct-v0.2:featherless-ai",  # Model chat tốt, nhanh
    "alternative": "microsoft/DialoGPT-large",  # Backup model
}

HEADERS = {"Authorization": f"Bearer {HF_API_TOKEN}"}

# ============ REQUEST MODELS ============
class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[Message]] = []
    model: Optional[str] = "default"

# ============ CHATBOT AI ============
@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        model_name = CHAT_MODELS.get(request.model, CHAT_MODELS["default"])

        # Chuẩn bị messages cho HF API
        messages_payload = [
            {"role": msg.role, "content": msg.content}
            for msg in request.conversation_history
        ]
        # Thêm message mới
        messages_payload.append({"role": "user", "content": request.message})

        payload = {
            "model": model_name,
            "messages": messages_payload,
            "stream": False
        }

        response = requests.post(
            "https://router.huggingface.co/v1/chat/completions",
            headers=HEADERS,
            json=payload,
            timeout=60
        )

        if response.status_code == 200:
            data = response.json()
            # HF trả về 'choices' -> 'message' -> 'content'
            generated_text = ""
            if "choices" in data and len(data["choices"]) > 0:
                generated_text = data["choices"][0]["message"]["content"]

            return {
                "success": True,
                "message": request.message,
                "response": generated_text,
                "model": model_name
            }
        elif response.status_code == 503:
            return {
                "success": False,
                "message": request.message,
                "response": "Model đang khởi động, vui lòng thử lại sau...",
                "error": "MODEL_LOADING"
            }
        else:
            return {
                "success": False,
                "message": request.message,
                "response": "Có lỗi xảy ra.",
                "error": response.text
            }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "message": request.message,
            "response": "Yêu cầu timeout. Vui lòng thử lại.",
            "error": "TIMEOUT"
        }
    except Exception as e:
        return {
            "success": False,
            "message": request.message,
            "response": f"Lỗi: {str(e)}",
            "error": str(e)
        }

def build_prompt(history: List[Message], current_message: str) -> str:
    """
    Xây dựng prompt từ lịch sử hội thoại
    """
    # System prompt cho chatbot về du lịch Việt Nam
    system_prompt = """You are a helpful AI assistant specializing in Vietnamese travel and tourism. 
You can answer questions about Vietnamese places, culture, food, weather, and provide travel recommendations.
Be friendly, informative, and concise. Answer in Vietnamese when user asks in Vietnamese, English when they ask in English."""
    
    # Format cho Mistral/Instruct models
    prompt = f"<s>[INST] {system_prompt}\n\n"
    
    # Thêm lịch sử hội thoại (giới hạn 3 tin nhắn gần nhất)
    recent_history = history[-6:] if len(history) > 6 else history
    
    for msg in recent_history:
        if msg.role == "user":
            prompt += f"User: {msg.content}\n"
        else:
            prompt += f"Assistant: {msg.content}\n"
    
    # Thêm câu hỏi hiện tại
    prompt += f"User: {current_message}\n[/INST]"
    
    return prompt

def clean_response(text: str, original_message: str) -> str:
    """
    Làm sạch response từ model
    """
    # Loại bỏ phần prompt nếu model trả về
    if "Assistant:" in text:
        text = text.split("Assistant:")[-1]
    
    if "[/INST]" in text:
        text = text.split("[/INST]")[-1]
    
    # Loại bỏ khoảng trắng thừa
    text = text.strip()
    
    # Nếu response rỗng hoặc quá ngắn
    if len(text) < 5:
        return "Xin lỗi, tôi không hiểu câu hỏi của bạn. Bạn có thể hỏi lại không?"
    
    return text

# ============ QA (giữ lại cho backward compatibility) ============
class QARequest(BaseModel):
    question: str
    context: str

@app.post("/api/qa")
async def answer_question(request: QARequest):
    """
    Trả lời câu hỏi dựa trên context được cung cấp
    """
    try:
        HF_QA_URL = "https://router.huggingface.co/models/deepset/roberta-base-squad2"
        
        payload = {
            "inputs": {
                "question": request.question,
                "context": request.context
            }
        }
        
        response = requests.post(
            HF_QA_URL,
            headers=HEADERS,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return {
                "success": True,
                "question": request.question,
                "answer": result.get("answer", "Không tìm thấy câu trả lời"),
                "score": result.get("score", 0)
            }
        else:
            print(f"HF API Error {response.status_code}: {response.text}")
            return {
                "success": False,
                "question": request.question,
                "answer": "Xin lỗi, không thể kết nối tới HuggingFace API. Vui lòng thử lại sau.",
                "score": 0
            }
            
    except Exception as e:
        print(f"QA Error: {str(e)}")
        return {
            "success": False,
            "question": request.question,
            "answer": f"Lỗi: {str(e)}",
            "score": 0
        }

# ============ HEALTH CHECK ============
@app.get("/health")
async def health_check():
    """Kiểm tra trạng thái API"""
    return {
        "status": "online",
        "service": "Vietnam Place Chatbot AI",
        "models": CHAT_MODELS
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)