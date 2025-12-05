@echo off
REM ================================
REM PAMS Ultra Quick Start (Windows)
REM Python 3.13 compatible - No ML initially
REM ================================

echo.
echo ================================
echo PAMS Ultra Quick Start
echo ================================
echo Setting up API only (no ML models yet)
echo.

cd /d "%~dp0"

REM Check Python
echo [1/4] Checking Python...
python --version
echo.

REM Setup Backend
echo [2/4] Setting up backend...
cd backend

echo Installing dependencies directly (no venv for speed)...
pip install --quiet -r requirements-ultra-minimal.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo Backend ready!

REM Start Backend
echo.
echo [3/4] Starting backend server...
echo.
echo ================================
echo BACKEND STARTING...
echo ================================
echo.

start /min cmd /c "cd /d %~dp0backend && python -m uvicorn main_simple:app --host 0.0.0.0 --port 8000 --reload"

echo Waiting for backend to start...
timeout /t 5 /nobreak >nul

REM Check Node.js
echo.
echo [4/4] Checking for Node.js (frontend)...
cd ..\frontend
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Node.js not found - skipping frontend.
    echo.
    echo ================================
    echo API IS RUNNING!
    echo ================================
    echo.
    echo Open in your browser:
    echo   http://localhost:8000/docs
    echo.
    goto :done
)

echo Installing frontend dependencies...
if not exist "node_modules" (
    call npm install
)

echo Starting frontend...
start /min cmd /c "cd /d %~dp0frontend && npm run dev"

timeout /t 5 /nobreak >nul

echo.
echo ================================
echo PAMS IS RUNNING!
echo ================================
echo.
echo Open in your browser:
echo   API: http://localhost:8000/docs
echo   Dashboard: http://localhost:3000
echo.

:done
echo Press any key to view the API in your browser...
pause >nul

start http://localhost:8000/docs

echo.
echo Services are running in the background.
echo To stop them, close this window or run: taskkill /F /IM python.exe
echo.
pause
