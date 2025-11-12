#!/bin/bash

echo "🚀 Starting Emotion Recognition Setup..."

# Check if venv exists, if not create it with Python 3.13
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment with Python 3.13..."
    if command -v python3.13 &> /dev/null; then
        python3.13 -m venv venv
    elif command -v python3 &> /dev/null; then
        python3 -m venv venv
    else
        echo "❌ Python 3 not found. Please install Python 3.10-3.13"
        exit 1
    fi
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip --quiet

# Install dependencies
echo "📥 Installing dependencies (this may take a few minutes)..."
pip install -r requirements.txt --upgrade

# Run the application
echo ""
echo "✅ Setup complete! Starting the application..."
echo "🌐 The web interface will open in your browser"
echo "⏳ Loading AI models (first run takes 1-2 minutes)..."
echo ""
python emotion_recognition.py
