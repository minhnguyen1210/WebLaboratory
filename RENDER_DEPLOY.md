# Hướng dẫn Deploy lên Render.com

## ✅ Ưu điểm Render.com
- ✅ **MIỄN PHÍ** - 750 giờ/tháng
- ✅ **KHÔNG có warning page** 
- ✅ **URL cố định** - không đổi mỗi lần deploy
- ✅ **Auto HTTPS** - SSL certificate miễn phí
- ✅ **Custom domain** (nếu muốn)
- ✅ **Auto deploy** từ GitHub

## 📋 Bước 1: Chuẩn bị

### 1.1 Tạo GitHub repository (nếu chưa có)
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/vietnam-place.git
git push -u origin main
```

## 🚀 Bước 2: Deploy lên Render

### 2.1 Tạo tài khoản
1. Truy cập: https://render.com
2. Sign up (dùng GitHub account để dễ dàng)

### 2.2 Tạo Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect GitHub repository của bạn
3. Cấu hình:
   - **Name**: `vietnam-place` (hoặc tên bạn muốn)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python start_render.py`
   - **Instance Type**: `Free`

### 2.3 Thêm Environment Variables
Click **"Environment"** → **"Add Environment Variable"**

Thêm các biến sau:

```
FIREBASE_API_KEY=AIzaSyBORzW2hqQe73zbpxBPIKiYbTmdfbvTXBw
FIREBASE_AUTH_DOMAIN=tesst-3a3fb.firebaseapp.com
FIREBASE_DATABASE_URL=https://tesst-3a3fb-default-rtdb.firebaseio.com
FIREBASE_PROJECT_ID=tesst-3a3fb
OPENWEATHER_API_KEY=a3091c751181373eb2659248e0ad1db5
HF_API_TOKEN=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
HF_API_BASE=http://localhost:8000
FLASK_ENV=production
```

### 2.4 Deploy
1. Click **"Create Web Service"**
2. Đợi 5-10 phút để build và deploy
3. URL của bạn: `https://vietnam-place.onrender.com` (hoặc tên bạn chọn)

## 🎉 Hoàn tất!

Website của bạn sẽ có URL dạng:
```
https://vietnam-place.onrender.com
```

- ✅ Không warning page
- ✅ HTTPS tự động
- ✅ URL cố định
- ✅ Hoạt động 24/7

## ⚠️ Lưu ý Free Tier

**Giới hạn:**
- Server tự động sleep sau 15 phút không hoạt động
- Lần truy cập đầu tiên sẽ mất 30-60 giây để wake up
- 750 giờ/tháng (đủ cho 1 app chạy full-time)

**Giải pháp:** 
- Nâng cấp lên Starter plan ($7/tháng) - server luôn chạy
- Hoặc dùng cron job để ping server mỗi 10 phút

## 🔄 Auto Deploy từ GitHub

Sau khi setup xong:
1. Mỗi khi push code lên GitHub
2. Render sẽ tự động deploy phiên bản mới
3. Không cần làm gì thêm!

## 🆘 Troubleshooting

### Nếu build failed:
- Check logs trong Render dashboard
- Đảm bảo `requirements.txt` đúng
- Đảm bảo tất cả file cần thiết đã commit vào Git

### Nếu app crash:
- Check logs trong Render dashboard
- Kiểm tra environment variables đã thêm đủ chưa
- Test local: `python start_render.py`

## 📊 Monitoring

Xem logs real-time:
1. Vào Render dashboard
2. Click vào service của bạn
3. Tab **"Logs"**
