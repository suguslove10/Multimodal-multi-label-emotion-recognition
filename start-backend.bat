@echo off
echo 🚀 Starting Backend API...

REM Check if venv exists
if not exist "venv\" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate venv
call venv\Scripts\activate.bat

REM Install backend dependencies
echo 📥 Installing backend dependencies...
pip install -r backend\requirements.txt --quiet

REM Start backend
echo ✅ Starting FastAPI server on http://localhost:8000
cd backend
python main.py
