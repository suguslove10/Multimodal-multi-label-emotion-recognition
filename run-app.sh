#!/bin/bash

echo "🚀 Starting Emotion Recognition App..."

# Activate venv
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3.13 -m venv venv
fi

source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q gradio transformers torch torchvision torchaudio pandas matplotlib Pillow scikit-learn

# Run app
echo "✅ Starting app..."
python app.py
