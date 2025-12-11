# 🚀 HƯỚNG DẪN DEPLOY WEB LÊN RENDER.COM - CHI TIẾT TỪNG BƯỚC

## PHẦN 1: CHUẨN BỊ

### ✅ Checklist trước khi bắt đầu:
- [x] Code đã push lên GitHub thành công
- [ ] Có tài khoản Render.com (miễn phí)
- [ ] Có các API keys cần thiết:
  - HuggingFace Token: https://huggingface.co/settings/tokens
  - Firebase Config: https://console.firebase.google.com
  - OpenWeather API: https://openweathermap.org/api

---

## PHẦN 2: TẠO TÀI KHOẢN VÀ KẾT NỐI GITHUB

### Bước 1: Đăng ký Render.com

1. Truy cập: **https://render.com**
2. Click nút **"Get Started"** hoặc **"Sign Up"**
3. Chọn **"Sign up with GitHub"** (khuyến nghị)
4. Cho phép Render truy cập GitHub của bạn
5. Hoàn tất đăng ký

### Bước 2: Kết nối Repository

1. Sau khi đăng nhập, bạn sẽ thấy Dashboard
2. Click **"New +"** ở góc trên bên phải
3. Chọn **"Web Service"**
4. Render sẽ hiển thị danh sách repositories từ GitHub
5. Tìm repository: **"WebLaboratory"**
6. Click nút **"Connect"** bên cạnh repository

---

## PHẦN 3: CÀI ĐẶT WEB SERVICE

### Bước 3: Cấu hình cơ bản

Sau khi click "Connect", bạn sẽ thấy form cấu hình. Điền như sau:

#### 📝 **Name**
```
vietnam-place
```
(Hoặc tên bạn muốn, sẽ tạo URL: https://vietnam-place.onrender.com)

#### 🌏 **Region**
```
Singapore
```
(Gần Việt Nam nhất, tốc độ tốt hơn)

#### 🌿 **Branch**
```
main
```

#### 🐍 **Runtime**
```
Python
```
(Render tự động detect)

#### 🔨 **Build Command**
```
pip install -r requirements.txt
```

#### ▶️ **Start Command**
```
gunicorn --bind 0.0.0.0:$PORT --timeout 120 --worker-class sync --workers 1 main:app
```

#### 💳 **Plan**
```
Free
```
(Chọn plan miễn phí)

---

## PHẦN 4: THÊM ENVIRONMENT VARIABLES (QUAN TRỌNG!)

### Bước 4: Mở phần Advanced

1. Kéo xuống, tìm mục **"Advanced"**
2. Click để mở rộng
3. Tìm mục **"Environment Variables"**
4. Click **"Add Environment Variable"**

### Bước 5: Thêm từng biến môi trường

#### 🔑 Biến 1: HF_API_TOKEN

**Cách lấy token:**
1. Vào https://huggingface.co/settings/tokens
2. Click **"New token"**
3. Name: `vietnam-place`
4. Type: **Read**
5. Click **"Generate"**
6. Copy token (dạng: `hf_xxxxxxxxxxxxx`)

**Nhập vào Render:**
- **Key**: `HF_API_TOKEN`
- **Value**: Paste token vừa copy (ví dụ: `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`)
- Click **"Add"**

---

#### 🔥 Biến 2-5: Firebase Config

**Cách lấy Firebase config:**
1. Vào https://console.firebase.google.com
2. Chọn project của bạn (hoặc tạo mới)
3. Click biểu tượng ⚙️ **Settings** → **Project settings**
4. Scroll xuống phần **"Your apps"**
5. Nếu chưa có app, click **"Add app"** → chọn **Web (</>) icon**
6. Đăng ký app, sẽ thấy config như này:

```javascript
const firebaseConfig = {
  apiKey: "AIzaSyBORzW2hqQe73zbpxBPIKiYbTmdfbvTXBw",
  authDomain: "tesst-3a3fb.firebaseapp.com",
  databaseURL: "https://tesst-3a3fb-default-rtdb.firebaseio.com",
  projectId: "tesst-3a3fb",
  storageBucket: "tesst-3a3fb.appspot.com"
};
```

**Nhập vào Render (4 biến):**

**Biến 2:**
- **Key**: `FIREBASE_API_KEY`
- **Value**: `AIzaSyBORzW2hqQe73zbpxBPIKiYbTmdfbvTXBw` (của bạn)

**Biến 3:**
- **Key**: `FIREBASE_AUTH_DOMAIN`
- **Value**: `tesst-3a3fb.firebaseapp.com` (của bạn)

**Biến 4:**
- **Key**: `FIREBASE_DATABASE_URL`
- **Value**: `https://tesst-3a3fb-default-rtdb.firebaseio.com` (của bạn)

**Biến 5:**
- **Key**: `FIREBASE_PROJECT_ID`
- **Value**: `tesst-3a3fb` (của bạn)

---

#### ☀️ Biến 6: OpenWeather API (Tùy chọn)

**Cách lấy:**
1. Vào https://openweathermap.org/api
2. Sign up miễn phí
3. Vào **API keys** tab
4. Copy key (hoặc tạo mới)

**Nhập vào Render:**
- **Key**: `OPENWEATHER_API_KEY`
- **Value**: Paste key của bạn

---

### 📋 Tổng kết Environment Variables:

Sau khi thêm xong, bạn sẽ có **6 biến**:
```
✅ HF_API_TOKEN
✅ FIREBASE_API_KEY
✅ FIREBASE_AUTH_DOMAIN
✅ FIREBASE_DATABASE_URL
✅ FIREBASE_PROJECT_ID
✅ OPENWEATHER_API_KEY (optional)
```

---

## PHẦN 5: DEPLOY!

### Bước 6: Bắt đầu deploy

1. Kiểm tra lại tất cả thông tin
2. Click nút **"Create Web Service"** ở cuối trang
3. Render sẽ bắt đầu build

### Bước 7: Theo dõi quá trình build

1. Bạn sẽ thấy màn hình logs
2. Quá trình build gồm:
   - ⏳ **Building...** (2-3 phút)
   - 📦 Cài đặt dependencies
   - 🚀 Starting service
   - ✅ **Live** (màu xanh)

**Logs thành công sẽ có:**
```
🌐 DEPLOYMENT MODE DETECTED (Render/Gunicorn)
🚀 Starting FastAPI backend on port 8000...
✅ FastAPI process started with PID: xxxx
✅ Flask app ready to serve requests
```

---

## PHẦN 6: KIỂM TRA VÀ TEST

### Bước 8: Lấy URL

1. Sau khi status chuyển sang **"Live"** (màu xanh)
2. Ở đầu trang, bạn sẽ thấy URL:
   ```
   https://vietnam-place.onrender.com
   ```
3. Copy URL này

### Bước 9: Test website

#### Test 1: Health Check
Vào URL:
```
https://vietnam-place.onrender.com/health
```

**Kết quả mong đợi:**
```json
{
  "status": "online",
  "models": {
    "chat": "mistralai/Mistral-7B-Instruct-v0.2",
    "qa": "deepset/roberta-base-squad2"
  }
}
```

#### Test 2: Website chính
Vào URL:
```
https://vietnam-place.onrender.com
```

**Kiểm tra:**
- ✅ Trang web load được
- ✅ Giao diện hiển thị đầy đủ
- ✅ Có thể tìm kiếm địa điểm

#### Test 3: Chatbot AI
1. Scroll xuống phần **"Hỏi AI về du lịch Việt Nam"**
2. Nhập câu hỏi: "Giới thiệu về Hà Nội"
3. Click **"Gửi"**
4. Đợi 20-30 giây (lần đầu model loading)
5. Chatbot sẽ trả lời

---

## PHẦN 7: LƯU Ý QUAN TRỌNG

### ⚠️ Free Tier Limitations:

1. **Service ngủ sau 15 phút idle**
   - Lần truy cập đầu sau khi ngủ mất 30-60 giây để wake up
   - Giải pháp: Dùng uptimerobot.com để ping định kỳ

2. **AI Model loading lần đầu**
   - Lần đầu hỏi chatbot mất 20-30 giây
   - Sau đó sẽ nhanh hơn

3. **750 giờ/tháng**
   - Đủ cho 1 service chạy cả tháng
   - Không cần thẻ tín dụng

### 🔧 Troubleshooting:

#### ❌ Build failed
**Nguyên nhân:** Lỗi cài đặt dependencies
**Giải pháp:**
1. Check logs để xem package nào lỗi
2. Kiểm tra `requirements.txt`
3. Đảm bảo `runtime.txt` có: `python-3.11.9`

#### ❌ Service crashed
**Nguyên nhân:** Thiếu environment variable
**Giải pháp:**
1. Vào **Environment** tab
2. Kiểm tra có đủ 6 biến không
3. Rebuild service: **Manual Deploy** → **Deploy latest commit**

#### ❌ Chatbot không trả lời
**Nguyên nhân:** `HF_API_TOKEN` không đúng hoặc hết quota
**Giải pháp:**
1. Check logs: tìm "⚠️ WARNING: HF_API_TOKEN"
2. Tạo token mới trên HuggingFace
3. Update trong Environment Variables
4. Rebuild

#### ❌ 503 Service Unavailable
**Nguyên nhân:** Service đang wake up hoặc FastAPI chưa start
**Giải pháp:**
- Đợi 30-60 giây và refresh
- Check logs xem có "✅ FastAPI process started" không

---

## PHẦN 8: CẬP NHẬT SAU NÀY

### Khi có thay đổi code:

1. **Push lên GitHub:**
   ```powershell
   git add .
   git commit -m "Update feature"
   git push origin main
   ```

2. **Auto-deploy:**
   - Render tự động detect thay đổi
   - Tự động build và deploy
   - Không cần làm gì thêm!

3. **Manual deploy (nếu cần):**
   - Vào Dashboard → Service
   - Click **"Manual Deploy"**
   - Chọn **"Deploy latest commit"**

---

## PHẦN 9: CHIA SẺ VỚI NGƯỜI KHÁC

### URL để chia sẻ:
```
https://vietnam-place.onrender.com
```

**Người dùng có thể:**
- ✅ Tìm kiếm địa điểm du lịch
- ✅ Xem thời tiết
- ✅ Chỉ đường giữa 2 địa điểm
- ✅ Dịch văn bản
- ✅ Hỏi chatbot AI
- ✅ Đăng ký/đăng nhập

**Lưu ý cho người dùng:**
- Lần đầu truy cập có thể chậm (wake up)
- Chatbot lần đầu hỏi mất 20-30 giây (loading model)
- Hoàn toàn miễn phí!

---

## 📊 MONITORING

### Xem logs real-time:
1. Vào Dashboard → Service của bạn
2. Tab **"Logs"**
3. Theo dõi requests, errors

### Xem metrics:
1. Tab **"Metrics"**
2. Xem CPU, Memory usage
3. Response time

---

## ✅ HOÀN TẤT!

**Chúc mừng! Website của bạn đã online:**
```
🌐 https://vietnam-place.onrender.com
```

**Các bước bạn đã làm:**
- [x] Tạo Web Service trên Render
- [x] Cấu hình build & start commands
- [x] Thêm 6 environment variables
- [x] Deploy thành công
- [x] Test chatbot AI
- [x] Sẵn sàng chia sẻ!

---

## 📝 GHI CHÚ

**Lưu thông tin này:**
- URL: `https://vietnam-place.onrender.com`
- Service Name: `vietnam-place`
- Region: `Singapore`
- Plan: `Free`

**Dashboard URL:**
```
https://dashboard.render.com/
```

---

🎉 **Bây giờ bạn có thể chia sẻ link cho bạn bè, đồng nghiệp, hoặc thêm vào CV!**
