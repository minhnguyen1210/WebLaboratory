/**
 * HuggingFace Chatbot Client
 * Real conversational AI - no context needed
 */

class HuggingFaceQAClient {
    constructor(apiBase = '') {
        this.apiBase = apiBase;
        this.isOnline = false;
        this.conversationHistory = [];
        this.checkConnection();
    }

    async checkConnection() {
        try {
            const response = await fetch(`${this.apiBase}/health`, {
                method: 'GET',
                headers: { 
                    'Content-Type': 'application/json',
                    'ngrok-skip-browser-warning': 'true',
                    'X-Pinggy-No-Screen': 'true'
                }
            });
            
            if (response.ok) {
                this.isOnline = true;
                const data = await response.json();
                console.log(`✅ HuggingFace API Online`);
                console.log(`📦 Models:`, data.models);
            } else {
                this.isOnline = false;
                console.warn('⚠️ HuggingFace API có vấn đề');
            }
        } catch (error) {
            this.isOnline = false;
            console.warn('❌ HuggingFace API Offline - Hãy khởi động backend server (python huggingface_api.py)');
        }
    }

    /**
     * Chat với AI - sử dụng Chat API endpoint
     * @param {string} message - Tin nhắn người dùng
     * @returns {Promise<Object>} - { success, message, response }
     */
    async chat(message) {
        if (!this.isOnline) {
            return {
                success: false,
                message: message,
                response: '❌ HuggingFace API không online. Hãy khởi động backend server:\n\npython -m uvicorn huggingface_api:app --host 0.0.0.0 --port 8000'
            };
        }

        try {
            const response = await fetch(`${this.apiBase}/api/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'ngrok-skip-browser-warning': 'true',
                    'X-Pinggy-No-Screen': 'true'
                },
                body: JSON.stringify({
                    message: message,
                    conversation_history: this.conversationHistory,
                    model: 'default'
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();
            
            // Lưu vào lịch sử hội thoại nếu thành công
            if (data.success) {
                this.conversationHistory.push({
                    role: "user",
                    content: message
                });
                this.conversationHistory.push({
                    role: "assistant",
                    content: data.response
                });
                
                // Giới hạn lịch sử (giữ 10 tin nhắn gần nhất)
                if (this.conversationHistory.length > 20) {
                    this.conversationHistory = this.conversationHistory.slice(-20);
                }
            }
            
            return data;
        } catch (error) {
            console.error('Error chatting:', error);
            return {
                success: false,
                message: message,
                response: `❌ Lỗi: ${error.message}`
            };
        }
    }

    /**
     * Xóa lịch sử hội thoại
     */
    clearHistory() {
        this.conversationHistory = [];
        console.log('🗑️ Đã xóa lịch sử hội thoại');
    }

    /**
     * Ask a question based on context (backward compatibility)
     * @param {string} question - The question to ask
     * @param {string} context - The context/document to search for answers
     * @returns {Promise<Object>} - { success, question, answer, score }
     */
    async askQuestion(question, context) {
        if (!this.isOnline) {
            return {
                success: false,
                question: question,
                answer: 'Lỗi: HuggingFace API không online. Hãy khởi động backend server.',
                score: 0
            };
        }

        try {
            const response = await fetch(`${this.apiBase}/api/qa`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'ngrok-skip-browser-warning': 'true',
                    'X-Pinggy-No-Screen': 'true'
                },
                body: JSON.stringify({
                    question: question,
                    context: context
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error asking question:', error);
            return {
                success: false,
                question: question,
                answer: `Lỗi: ${error.message}`,
                score: 0
            };
        }
    }
}

// Create global instance
const hfClient = new HuggingFaceQAClient();