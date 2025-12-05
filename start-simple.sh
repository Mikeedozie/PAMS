#!/bin/bash

echo "========================================"
echo "PAMS Quick Start Setup"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.11+ from https://www.python.org/"
    exit 1
fi

echo "Step 1: Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

echo ""
echo "Step 2: Activating virtual environment..."
source venv/bin/activate

echo ""
echo "Step 3: Installing minimal dependencies..."
pip install -q --upgrade pip
pip install -q -r backend/requirements-minimal.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
echo "✓ Dependencies installed"

echo ""
echo "Step 4: Starting PAMS backend server..."
echo ""
echo "========================================"
echo "🚀 PAMS is starting..."
echo "========================================"
echo ""
echo "Access the application at:"
echo "  - API Documentation: http://localhost:8000/docs"
echo "  - Home: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python -m uvicorn backend.main_simple:app --reload --host 0.0.0.0 --port 8000
