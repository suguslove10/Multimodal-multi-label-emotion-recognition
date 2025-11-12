# 🎭 AI-Powered Multimodal Emotion Recognition

Modern full-stack emotion recognition application using Next.js, FastAPI, and state-of-the-art AI models.

![Tech Stack](https://img.shields.io/badge/Next.js-16-black)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)
![Python](https://img.shields.io/badge/Python-3.10--3.13-blue)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue)

## ✨ Features

- 🎨 **Modern UI** - Beautiful gradient design with Tailwind CSS v4
- 📝 **Text Analysis** - Emotion detection from written text
- 📸 **Image Upload** - Facial emotion analysis from photos
- 🎤 **Voice Analysis** - Audio recording and voice tone emotion detection
- 🤖 **Machine Learning** - Decision Tree and KNN predictions
- 📊 **Visualizations** - Interactive confidence charts
- 💾 **History Tracking** - Save and review past analyses

## 🚀 Quick Start

### Prerequisites

- Python 3.10-3.13 (NOT 3.14)
- Node.js 18+ and npm
- Microphone access
- 2-3 GB disk space for AI models

### Installation & Run

**1. Start Backend (Terminal 1):**
```bash
# Mac/Linux
./start-backend.sh

# Windows
start-backend.bat
```

**2. Start Frontend (Terminal 2):**
```bash
# Mac/Linux
./start-frontend.sh

# Windows
start-frontend.bat
```

**3. Open Browser:**
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

## 📖 Usage

1. **Text:** Type how you're feeling in the text box
2. **Image:** Click "Upload" and select a photo (or use "Camera" if available)
3. **Audio:** Click "Start Recording", speak for 5-10 seconds, then click "Stop"
4. **Analyze:** Click "Analyze Emotions" button
5. **Results:** View emotion breakdown, confidence chart, and ML predictions

## 🏗️ Architecture

```
┌─────────────────┐         ┌─────────────────┐
│   Next.js UI    │ ◄─────► │  FastAPI Server │
│  (Port 3000)    │  HTTP   │   (Port 8000)   │
└─────────────────┘         └─────────────────┘
                                     │
                            ┌────────┴────────┐
                            │   AI Models     │
                            │  - Text (RoBERTa)│
                            │  - Image (ViT)  │
                            │  - Audio (Wav2Vec2)│
                            └─────────────────┘
```

## 🛠️ Tech Stack

### Frontend
- Next.js 16 (App Router, Turbopack)
- TypeScript
- Tailwind CSS v4
- Lucide React Icons

### Backend
- FastAPI
- Hugging Face Transformers
- PyTorch
- Scikit-learn (Decision Tree, KNN)
- Pandas & Matplotlib

### AI Models
- **Text:** `j-hartmann/emotion-english-distilroberta-base`
- **Image:** `trpakov/vit-face-expression`
- **Audio:** `ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition`

## 📁 Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI server & AI logic
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── app/
│   │   ├── page.tsx        # Main UI component
│   │   ├── layout.tsx      # Root layout
│   │   └── globals.css     # Global styles
│   └── package.json
├── start-backend.sh         # Backend startup (Mac/Linux)
├── start-frontend.sh        # Frontend startup (Mac/Linux)
├── start-backend.bat        # Backend startup (Windows)
├── start-frontend.bat       # Frontend startup (Windows)
└── README.md
```

## 🐛 Troubleshooting

**Backend won't start:**
- Check Python version: `python3 --version` (must be 3.10-3.13)
- Recreate venv: `rm -rf venv && python3.13 -m venv venv`
- First run downloads ~1-2GB of AI models (takes 1-2 minutes)

**Frontend won't start:**
- Check Node.js: `node --version` (must be 18+)
- Reinstall: `cd frontend && rm -rf node_modules && npm install`

**Analysis fails:**
- Ensure backend shows "✅ Models loaded successfully"
- Check backend is running on port 8000
- Check browser console (F12) for errors

**Audio not working:**
- Grant microphone permissions in browser
- Speak clearly for 5-10 seconds
- Use Chrome or Edge for best compatibility

## 📊 API Endpoints

- `GET /` - Health check
- `GET /health` - Models status
- `POST /analyze` - Analyze emotions (multipart/form-data)
  - `text`: string
  - `image`: file
  - `audio`: file
- `GET /history?limit=10` - Get analysis history

## 🚀 Deployment

### Backend (Railway/Render/AWS)
```bash
pip install -r backend/requirements.txt
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

### Frontend (Vercel - Recommended)
```bash
cd frontend
npm run build
```
Set environment variable: `NEXT_PUBLIC_API_URL=https://your-backend-url.com`

## 📝 License

MIT License

## 🙏 Acknowledgments

- Hugging Face for pre-trained models
- Next.js and FastAPI teams
- Open source community

---

**Made with ❤️ using Next.js, FastAPI, and AI**
