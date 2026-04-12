@echo off
REM FastAPI Server Launcher
REM ========================

echo.
echo ====================================================
echo     Face ^& Emotion Detection API - FastAPI
echo ====================================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo [*] Python version:
python --version
echo.

REM Check if running from correct directory
if not exist "app\main.py" (
    echo ERROR: run.bat must be executed from project root directory
    echo Please ensure app\main.py exists
    pause
    exit /b 1
)

echo [*] Starting FastAPI Server...
echo.
echo 🌐 API will be available at:
echo    - http://127.0.0.1:8000
echo    - Docs: http://127.0.0.1:8000/docs
echo.

REM Run the application
python run.py

pause
