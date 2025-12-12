# HƯỚNG DẪN DEPLOY WEB LÊN RENDER.COM - CHI TIẾT TỪNG BƯỚC

## PHẦN 1: CHUẨN BỊ

###  Checklist trước khi bắt đầu:
- Code đã push lên GitHub thành công
- Có tài khoản Render.com (miễn phí)
- Có các API keys cần thiết:
  - HuggingFace Token: https://huggingface.co/settings/tokens
  - Firebase Config: https://console.firebase.google.com
  - OpenWeather API: https://openweathermap.org/api

---

## PHẦN 2: TẠO TÀI KHOẢN VÀ KẾT NỐI GITHUB

### Bước 1: Đăng ký Render.com

1. Truy cập: **https://render.com**
2. Click nút **"Get Started"** hoặc **"Sign Up"**
3. Chọn **"Sign up with GitHub"** 
4. Cho phép Render truy cập GitHub 
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

Sau khi click "Connect". Điền như sau:

####  **Name**
####  **Region**
####  **Branch**
```
main
```
#### 🐍 **Runtime**
```
Python
```

####  **Build Command**
```
pip install -r requirements.txt
```

####  **Start Command**
```
gunicorn --bind 0.0.0.0:$PORT --timeout 120 --worker-class sync --workers 1 main:app
```

## PHẦN 4: THÊM ENVIRONMENT VARIABLES 

### Bước 4: Mở phần Advanced

1. Kéo xuống, tìm mục **"Advanced"**
2. Click để mở rộng
3. Tìm mục **"Environment Variables"**
4. Click **"Add Environment Variable"**

### Bước 5: Thêm từng biến môi trường

####  Biến 1: HF_API_TOKEN

**Cách lấy token:**
1. Vào https://huggingface.co/settings/tokens
2. Click **"New token"**
3. Name: `vietnam-place`
4. Type: **Read**
5. Click **"Generate"**
6. Copy token (dạng: `hf_xxxxxxxxxxxxx`)

**Nhập vào Render:**
- **Key**: `HF_API_TOKEN`
- **Value**: Paste token vừa copy
- Click **"Add"**

---

####  Biến 2-5: Firebase Config

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

**Biến 3:**
- **Key**: `FIREBASE_AUTH_DOMAIN`

**Biến 4:**
- **Key**: `FIREBASE_DATABASE_URL`

**Biến 5:**
- **Key**: `FIREBASE_PROJECT_ID`

---
####  Biến 6: OpenWeather API 

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
 HF_API_TOKEN
 FIREBASE_API_KEY
 FIREBASE_AUTH_DOMAIN
 FIREBASE_DATABASE_URL
 FIREBASE_PROJECT_ID
 OPENWEATHER_API_KEY (optional)
```
---

## PHẦN 5: DEPLOY!

### Bước 6: Bắt đầu deploy

1. Kiểm tra lại tất cả thông tin
2. Click nút **"Create Web Service"** ở cuối trang
3. Render sẽ bắt đầu build

### Bước 7: Theo dõi quá trình build

## PHẦN 6: KIỂM TRA VÀ TEST

### Bước 8: Lấy URL

1. Sau khi status chuyển sang **"Live"** (màu xanh)
2. Ở đầu trang, bạn sẽ thấy URL:
   ```
   https://vietnam-place.onrender.com
   ```
3. Copy URL này

## PHẦN 7: LƯU Ý QUAN TRỌNG

###  Free Tier Limitations:

1. **Service ngủ sau 15 phút idle**
   - Lần truy cập đầu sau khi ngủ mất 30-60 giây để wake up
   - Giải pháp: Dùng uptimerobot.com để ping định kỳ

2. **AI Model loading lần đầu**
   - Lần đầu hỏi chatbot mất 20-30 giây
   - Sau đó sẽ nhanh hơn
