# 🎭 AI-Powered Multimodal Emotion Recognition

Modern full-stack emotion recognition application using Next.js, FastAPI, and state-of-the-art AI models.

![Tech Stack](https://img.shields.io/badge/Next.js-14-black)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)
![Python](https://img.shields.io/badge/Python-3.10--3.13-blue)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue)

## ✨ Features

- 🎨 **Modern UI** - Beautiful gradient design with Tailwind CSS
- 📝 **Text Analysis** - Emotion detection from written text
- 📸 **Facial Recognition** - Real-time webcam capture and facial emotion analysis
- 🎤 **Voice Analysis** - Audio recording and voice tone emotion detection
- 🤖 **Machine Learning** - Decision Tree and KNN predictions
- 📊 **Visualizations** - Interactive confidence charts
- 💾 **History Tracking** - Save and review past analyses

## 🚀 Quick Start

### Prerequisites

- Python 3.10-3.13 (NOT 3.14)
- Node.js 18+ and npm
- Webcam and microphone
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
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 📖 Usage

1. Enter text describing your emotions
2. Capture or upload a photo showing your facial expression
3. Record a short audio clip (5-10 seconds)
4. Click "Analyze Emotions"
5. View detailed results with confidence scores

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
- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Icons:** Lucide React
- **Features:** Webcam/mic capture, file uploads

### Backend
- **Framework:** FastAPI
- **AI Models:** Hugging Face Transformers
- **Deep Learning:** PyTorch
- **ML Algorithms:** Scikit-learn (Decision Tree, KNN)
- **Data:** Pandas, Matplotlib

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
│   │   └── page.tsx        # Main UI component
│   ├── package.json
│   └── tailwind.config.ts
├── start-backend.sh         # Backend startup (Mac/Linux)
├── start-frontend.sh        # Frontend startup (Mac/Linux)
├── start-backend.bat        # Backend startup (Windows)
├── start-frontend.bat       # Frontend startup (Windows)
└── README.md               # This file
```

## 🔧 Development

### Backend Development
```bash
source venv/bin/activate
cd backend
uvicorn main:app --reload --port 8000
```

### Frontend Development
```bash
cd frontend
npm run dev
```

## 🐛 Troubleshooting

**Backend Issues:**
- Ensure Python 3.10-3.13 is installed
- Check if port 8000 is available
- First run downloads ~1-2GB of AI models

**Frontend Issues:**
- Ensure Node.js 18+ is installed
- Delete `node_modules` and run `npm install`
- Check if port 3000 is available

**Camera/Mic Issues:**
- Grant browser permissions
- Use Chrome/Edge (best compatibility)
- Ensure HTTPS or localhost

## 📊 API Endpoints

- `GET /` - Health check
- `POST /analyze` - Analyze emotions (multipart/form-data)
- `GET /history?limit=10` - Get analysis history
- `GET /docs` - Interactive API documentation

## 🚀 Deployment

### Backend (Railway/Render)
```bash
pip install -r backend/requirements.txt
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

### Frontend (Vercel)
```bash
cd frontend
npm run build
```

Update API URL in environment variables.

## 📝 License

MIT License - Free for personal and commercial use

## 🤝 Contributing

Contributions welcome! Please open an issue or submit a PR.

## 🙏 Acknowledgments

- Hugging Face for pre-trained models
- Next.js and FastAPI teams
- Open source community

---

Made with ❤️ using Next.js, FastAPI, and AI
