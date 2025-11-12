# 🎭 AI Emotion Recognition - Next.js + FastAPI

Modern full-stack emotion recognition app with professional UI.

## 🏗️ Architecture

- **Frontend:** Next.js 14 + TypeScript + Tailwind CSS
- **Backend:** FastAPI + Python AI models
- **Features:** Real-time webcam/mic capture, multimodal analysis

## 🚀 Quick Start

### Option 1: Run Both Servers (Recommended)

**Terminal 1 - Backend:**
```bash
./start-backend.sh    # Mac/Linux
start-backend.bat     # Windows
```

**Terminal 2 - Frontend:**
```bash
./start-frontend.sh   # Mac/Linux
start-frontend.bat    # Windows
```

### Option 2: Manual Start

**Backend:**
```bash
source venv/bin/activate
pip install -r backend/requirements.txt
cd backend && python main.py
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 📱 Access

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

## ⏱️ First Run

- Backend takes 1-2 minutes to download AI models (~1-2 GB)
- Frontend installs dependencies automatically
- Subsequent runs are much faster

## 🎯 How to Use

1. Open http://localhost:3000 in your browser
2. Enter text describing your emotions
3. Capture/upload a photo (facial expression)
4. Record audio (5-10 seconds)
5. Click "Analyze Emotions"
6. View results with confidence scores and ML predictions

## 📋 Requirements

- Python 3.10-3.13 (NOT 3.14)
- Node.js 18+ and npm
- Webcam and microphone
- 2-3 GB disk space for AI models

## 🛠️ Tech Stack

### Frontend
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- Lucide React (icons)

### Backend
- FastAPI
- Transformers (Hugging Face)
- PyTorch
- Scikit-learn
- Pandas & Matplotlib

## 🔧 Troubleshooting

**Backend won't start:**
- Check Python version (3.10-3.13)
- Ensure virtual environment is activated
- Check if port 8000 is available

**Frontend won't start:**
- Check Node.js version (18+)
- Delete `node_modules` and run `npm install`
- Check if port 3000 is available

**CORS errors:**
- Make sure backend is running on port 8000
- Check CORS settings in `backend/main.py`

**Camera/Mic not working:**
- Check browser permissions
- Use HTTPS or localhost only
- Try different browser (Chrome recommended)

## 📁 Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI server
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── app/
│   │   └── page.tsx        # Main UI component
│   ├── package.json
│   └── tailwind.config.ts
├── start-backend.sh         # Backend startup (Mac/Linux)
├── start-frontend.sh        # Frontend startup (Mac/Linux)
├── start-backend.bat        # Backend startup (Windows)
└── start-frontend.bat       # Frontend startup (Windows)
```

## 🎨 Features

✅ Modern, responsive UI with gradient design
✅ Real-time webcam capture
✅ Audio recording with visual feedback
✅ Multimodal emotion analysis (text, image, audio)
✅ Interactive confidence charts
✅ Machine learning predictions (Decision Tree, KNN)
✅ Analysis history tracking
✅ Cross-platform support

## 🚀 Production Deployment

**Backend:**
- Deploy to Railway, Render, or AWS
- Set environment variables
- Use production ASGI server (Gunicorn + Uvicorn)

**Frontend:**
- Deploy to Vercel (recommended)
- Update API URL in environment variables
- Enable HTTPS

## 📝 License

MIT License - Feel free to use for personal or commercial projects
