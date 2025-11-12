# 🚀 Getting Started

## What You Have

A professional full-stack emotion recognition app with:
- ✅ Modern Next.js frontend with beautiful UI
- ✅ FastAPI backend with AI models
- ✅ Real-time webcam and microphone capture
- ✅ Multimodal emotion analysis
- ✅ Machine learning predictions

## How to Run

### Step 1: Start Backend (Terminal 1)

**Mac/Linux:**
```bash
./start-backend.sh
```

**Windows:**
```
start-backend.bat
```

Wait for: `✅ Models loaded successfully`

### Step 2: Start Frontend (Terminal 2)

**Mac/Linux:**
```bash
./start-frontend.sh
```

**Windows:**
```
start-frontend.bat
```

Wait for: `✓ Ready in...`

### Step 3: Open Browser

Go to: **http://localhost:3000**

## First Time Setup

⏱️ **First run takes 1-2 minutes** to download AI models (~1-2GB)

The backend will download:
- Text emotion model (~330MB)
- Facial expression model (~330MB)
- Voice emotion model (~1.2GB)

These are cached, so subsequent runs are instant!

## Using the App

1. **Enter Text:** Type how you're feeling
2. **Capture Photo:** 
   - Click "Open Camera" → "Capture"
   - Or click "Upload Photo" to use existing image
3. **Record Audio:**
   - Click "Start Recording"
   - Speak for 5-10 seconds
   - Click "Stop Recording"
4. **Analyze:** Click "Analyze Emotions"
5. **View Results:** See emotion breakdown and ML predictions

## Troubleshooting

### Backend won't start
```bash
# Check Python version (must be 3.10-3.13)
python3 --version

# Recreate virtual environment
rm -rf venv
python3.13 -m venv venv
./start-backend.sh
```

### Frontend won't start
```bash
# Reinstall dependencies
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Camera/Mic not working
- Grant browser permissions when prompted
- Use Chrome or Edge (best compatibility)
- Ensure you're on localhost or HTTPS

### Port already in use
```bash
# Kill process on port 8000 (backend)
lsof -ti:8000 | xargs kill -9

# Kill process on port 3000 (frontend)
lsof -ti:3000 | xargs kill -9
```

## Stopping the Servers

Press `Ctrl+C` in each terminal window

## What's Next?

- Try different emotions and expressions
- Check the analysis history
- View ML predictions improving over time
- Export your data as CSV

## Need Help?

Check:
- `README.md` - Full documentation
- `http://localhost:8000/docs` - API documentation
- GitHub issues

---

Enjoy your AI emotion recognition app! 🎭✨
