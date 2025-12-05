@echo off
echo ========================================
echo PAMS Quick Start Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11+ from https://www.python.org/
    pause
    exit /b 1
)

echo Step 1: Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)

echo.
echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Step 3: Installing minimal dependencies...
pip install -q --upgrade pip
pip install -q -r backend\requirements-minimal.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed

echo.
echo Step 4: Starting PAMS backend server...
echo.
echo ========================================
echo 🚀 PAMS is starting...
echo ========================================
echo.
echo Access the application at:
echo   - API Documentation: http://localhost:8000/docs
echo   - Home: http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo.

python -m uvicorn backend.main_simple:app --reload --host 0.0.0.0 --port 8000
