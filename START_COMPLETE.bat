@echo off
echo ============================================
echo   PAMS - Complete System Startup
echo ============================================
echo.
echo This will start:
echo   1. Backend API Server (Port 8000)
echo   2. Frontend Web Interface (Port 3000)
echo.
echo Press Ctrl+C in each window to stop the servers
echo.
pause

echo.
echo [1/2] Starting Backend Server...
start cmd /k "cd /d %~dp0 && python -m pip install --quiet fastapi uvicorn sqlalchemy pydantic pydantic-settings python-dotenv pandas numpy scikit-learn && python -m uvicorn backend.main_simple:app --reload --host 127.0.0.1 --port 8000"

timeout /t 3 /nobreak >nul

echo.
echo [2/2] Starting Frontend Server...
start cmd /k "cd /d %~dp0frontend && npm install && echo. && echo Installing UI dependencies... && npm install lucide-react recharts @headlessui/react clsx tailwind-merge && echo. && echo Starting development server... && npm run dev"

echo.
echo ============================================
echo   PAMS is starting up!
echo ============================================
echo.
echo Backend API:        http://localhost:8000/docs
echo Frontend Interface: http://localhost:3000/landing
echo.
echo Wait 10-20 seconds for both servers to fully start
echo Then open your browser to: http://localhost:3000/landing
echo.
echo Press any key to exit this window (servers will keep running)...
pause >nul
