# PAMS Quick Start - PowerShell Version
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "PAMS Quick Start Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Navigate to project directory
Set-Location "C:\Users\Edozie\Downloads\MalwareIntel-ed\PAMS"

# Check Python
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.11+" -ForegroundColor Red
    pause
    exit 1
}

Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Yellow
python -m pip install --quiet --upgrade pip
python -m pip install --quiet fastapi uvicorn sqlalchemy pydantic pydantic-settings python-dotenv pandas numpy scikit-learn

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
    pause
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "🚀 Starting PAMS Backend Server..." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Access the application at:" -ForegroundColor Cyan
Write-Host "  📊 API Documentation: http://localhost:8000/docs" -ForegroundColor White
Write-Host "  🏠 Home: http://localhost:8000" -ForegroundColor White
Write-Host "  ❤️  Health Check: http://localhost:8000/health" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start the server
python -m uvicorn backend.main_simple:app --reload --host 0.0.0.0 --port 8000
