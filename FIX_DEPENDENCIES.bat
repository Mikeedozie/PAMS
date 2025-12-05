@echo off
cls
echo ========================================================
echo   PAMS - Quick Fix for Missing Dependencies
echo ========================================================
echo.
echo This will install the missing UI components
echo (lucide-react, recharts, headlessui, etc.)
echo.
pause

cd frontend

echo.
echo [1/3] Installing lucide-react (icons)...
call npm install lucide-react

echo.
echo [2/3] Installing recharts (charts)...
call npm install recharts

echo.
echo [3/3] Installing headlessui and utilities...
call npm install @headlessui/react clsx tailwind-merge

echo.
echo ========================================================
echo   ✓ All dependencies installed successfully!
echo ========================================================
echo.
echo Now you can run the frontend with: npm run dev
echo Or just double-click START_COMPLETE.bat
echo.
pause
