#!/bin/bash

echo "🚀 Starting Backend API..."

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    if command -v python3.13 &> /dev/null; then
        python3.13 -m venv venv
    elif command -v python3 &> /dev/null; then
        python3 -m venv venv
    else
        echo "❌ Python 3 not found"
        exit 1
    fi
fi

# Activate venv
source venv/bin/activate

# Install backend dependencies
echo "📥 Installing backend dependencies..."
pip install -r backend/requirements.txt --quiet

# Start backend
echo "✅ Starting FastAPI server on http://localhost:8000"
cd backend && python main.py
