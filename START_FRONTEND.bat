@echo off
echo ============================================
echo   PAMS Frontend - Starting Development Server
echo ============================================
echo.

cd frontend

echo [1/2] Installing dependencies...
call npm install

echo.
echo [2/2] Starting Next.js development server...
echo.
echo Frontend will be available at: http://localhost:3000
echo.
echo Available pages:
echo   - Landing Page:     http://localhost:3000/landing
echo   - User Dashboard:   http://localhost:3000/dashboard
echo   - Admin Panel:      http://localhost:3000/admin
echo.

call npm run dev
