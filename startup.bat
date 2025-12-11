@echo off
REM Script khởi động cho Vietnam Place
REM Chạy cả FastAPI và Flask servers

setlocal enabledelayedexpansion

cls
echo.
echo ================================
echo Vietnam Place - Starting Servers
echo ================================
echo.

REM Kiểm tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python first.
    pause
    exit /b 1
)

echo [OK] Python installed

REM Kiểm tra .env file
if not exist ".env" (
    echo [WARNING] .env file not found
    echo [INFO] Creating from .env.example...
    if exist ".env.example" (
        copy .env.example .env
        echo [INFO] Please edit .env file with your credentials
    )
)

REM Cài dependencies
echo [INFO] Installing dependencies...
python -m pip install -q --upgrade pip
python -m pip install -q -r requirements.txt
echo [OK] Dependencies installed

echo.
echo Starting FastAPI backend on port 8000...
start "FastAPI Backend" cmd /k "title FastAPI Backend & uvicorn huggingface_api:app --reload --host 0.0.0.0 --port 8000"

timeout /t 3

echo Starting Flask backend on port 5000...
start "Flask Backend" cmd /k "title Flask Backend & python main.py"

timeout /t 3

echo.
echo ================================
echo All servers are starting!
echo ================================
echo.
echo Website:     http://localhost:5000
echo FastAPI:    http://localhost:8000
echo Docs:       http://localhost:8000/docs
echo.
echo To expose with ngrok:
echo   ngrok http 8000 (for FastAPI)
echo   ngrok http 5000 (for Flask)
echo.
pause
