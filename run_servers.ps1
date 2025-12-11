# Script PowerShell để khởi động cả FastAPI và Flask servers

Write-Host "🚀 Vietnam Place - Starting Servers" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan

# Kiểm tra xem Python đã cài đặt chưa
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Python không được cài đặt hoặc không trong PATH" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Python: $pythonVersion" -ForegroundColor Green

# Kiểm tra .env file
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  File .env không tìm thấy" -ForegroundColor Yellow
    Write-Host "📋 Tạo .env file từ .env.example..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "⚠️  Vui lòng điền thông tin vào file .env" -ForegroundColor Yellow
}

# Kiểm tra requirements.txt
if (-not (Test-Path "requirements.txt")) {
    Write-Host "❌ requirements.txt không tìm thấy" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "📦 Kiểm tra dependencies..." -ForegroundColor Cyan
python -m pip install -q --upgrade pip
python -m pip install -q -r requirements.txt

Write-Host ""
Write-Host "✅ Các dependencies đã được cài đặt" -ForegroundColor Green
Write-Host ""

# Khởi động FastAPI backend
Write-Host "🔧 Khởi động FastAPI Backend (port 8000)..." -ForegroundColor Cyan
Write-Host "   Uvicorn: http://localhost:8000" -ForegroundColor Gray
Write-Host "   Docs: http://localhost:8000/docs" -ForegroundColor Gray

$fastapiJob = Start-Job -ScriptBlock {
    Set-Location $args[0]
    uvicorn huggingface_api:app --reload --host 0.0.0.0 --port 8000
} -ArgumentList $PWD

Start-Sleep -Seconds 3

# Kiểm tra xem FastAPI đã start chưa
$fastapiRunning = Get-Job $fastapiJob | Select-Object -ExpandProperty State
if ($fastapiRunning -eq "Running") {
    Write-Host "✅ FastAPI Backend đang chạy (PID: $($fastapiJob.Id))" -ForegroundColor Green
} else {
    Write-Host "❌ FastAPI Backend không khởi động được" -ForegroundColor Red
    Get-Job $fastapiJob | Stop-Job
    exit 1
}

Write-Host ""

# Khởi động Flask backend
Write-Host "🔧 Khởi động Flask Backend (port 5000)..." -ForegroundColor Cyan
Write-Host "   Website: http://localhost:5000" -ForegroundColor Gray

$flaskJob = Start-Job -ScriptBlock {
    Set-Location $args[0]
    python main.py
} -ArgumentList $PWD

Start-Sleep -Seconds 3

# Kiểm tra xem Flask đã start chưa
$flaskRunning = Get-Job $flaskJob | Select-Object -ExpandProperty State
if ($flaskRunning -eq "Running") {
    Write-Host "✅ Flask Backend đang chạy (PID: $($flaskJob.Id))" -ForegroundColor Green
} else {
    Write-Host "❌ Flask Backend không khởi động được" -ForegroundColor Red
    Get-Job $fastapiJob | Stop-Job
    Get-Job $flaskJob | Stop-Job
    exit 1
}

Write-Host ""
Write-Host "=================================" -ForegroundColor Cyan
Write-Host "🎉 Tất cả servers đang chạy!" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📱 Truy cập website: http://localhost:5000" -ForegroundColor Cyan
Write-Host "📚 FastAPI docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 Để expose qua ngrok:" -ForegroundColor Yellow
Write-Host "   ngrok http 8000  (for FastAPI)" -ForegroundColor Gray
Write-Host "   ngrok http 5000  (for Flask)" -ForegroundColor Gray
Write-Host ""
Write-Host "⏹️  Bấm Ctrl+C để dừng" -ForegroundColor Yellow
Write-Host ""

# Giữ script chạy
try {
    while ($true) {
        Start-Sleep -Seconds 1
        
        # Kiểm tra xem các jobs có còn chạy không
        if ((Get-Job $fastapiJob).State -ne "Running") {
            Write-Host "⚠️  FastAPI Backend đã dừng" -ForegroundColor Yellow
        }
        if ((Get-Job $flaskJob).State -ne "Running") {
            Write-Host "⚠️  Flask Backend đã dừng" -ForegroundColor Yellow
        }
    }
} catch {
    Write-Host ""
    Write-Host "🛑 Dừng servers..." -ForegroundColor Red
    Get-Job $fastapiJob | Stop-Job
    Get-Job $flaskJob | Stop-Job
    Get-Job $fastapiJob | Remove-Job
    Get-Job $flaskJob | Remove-Job
    Write-Host "✅ Servers đã dừng" -ForegroundColor Green
}
