@echo off
echo 🚀 Starting Emotion Recognition Setup...

REM Check if venv exists, if not create it
if not exist "venv\" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Python not found. Please install Python 3.10-3.13
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️  Upgrading pip...
python -m pip install --upgrade pip --quiet

REM Install dependencies
echo 📥 Installing dependencies (this may take a few minutes)...
pip install -r requirements.txt --upgrade

REM Run the application
echo.
echo ✅ Setup complete! Starting the application...
echo 🌐 The web interface will open in your browser
echo ⏳ Loading AI models (first run takes 1-2 minutes)...
echo.
python emotion_recognition.py

pause
