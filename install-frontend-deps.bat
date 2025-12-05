@echo off
echo ============================================
echo   Installing Frontend Dependencies
echo ============================================
echo.

cd frontend

echo Installing required packages...
echo.
call npm install lucide-react recharts @headlessui/react clsx tailwind-merge

echo.
echo ============================================
echo   Installation Complete!
echo ============================================
echo.
echo You can now run: npm run dev
echo.
pause
