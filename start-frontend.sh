#!/bin/bash

# Navigate to frontend directory
cd "$(dirname "$0")/frontend"

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

# Start the development server
echo "Starting PAMS frontend..."
echo "Dashboard will be available at: http://localhost:3000"
echo ""
npm run dev
