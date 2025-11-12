@echo off
echo 🚀 Starting Frontend...

cd frontend

REM Install dependencies if needed
if not exist "node_modules\" (
    echo 📥 Installing frontend dependencies...
    npm install
)

REM Start Next.js dev server
echo ✅ Starting Next.js on http://localhost:3000
npm run dev
