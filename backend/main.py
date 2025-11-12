from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline
import torch
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from PIL import Image
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
import os
import time
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

app = FastAPI(title="Emotion Recognition API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup
CSV_FILE = "emotion_results.csv"
DEVICE = 0 if torch.cuda.is_available() else -1

# Create CSV if not exists
if not os.path.exists(CSV_FILE):
    pd.DataFrame(columns=["timestamp","text","text_label","text_score",
                          "image_label","image_score","audio_label","audio_score"]).to_csv(CSV_FILE, index=False)

# Load models
print("Loading AI models...")
text_pipe = pipeline("text-classification",
                     model="j-hartmann/emotion-english-distilroberta-base",
                     device=DEVICE)
image_pipe = pipeline("image-classification",
                      model="trpakov/vit-face-expression",
                      top_k=5,
                      device=DEVICE)
audio_pipe = pipeline("audio-classification",
                      model="ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition",
                      top_k=6,
                      device=DEVICE)
print("✅ Models loaded successfully")

def analyze_text(text: str):
    try:
        res = text_pipe(text)
        if isinstance(res, list): res = res[0]
        return str(res["label"]).title(), float(res["score"])
    except:
        return "Neutral", 0.0

def analyze_image(img: Image.Image):
    try:
        res = image_pipe(img)
        if isinstance(res, list) and len(res) > 0:
            return str(res[0]["label"]).title(), float(res[0]["score"])
        return "Neutral", 0.0
    except:
        return "Neutral", 0.0

def analyze_audio(audio_path: str):
    try:
        import librosa
        import soundfile as sf
        
        # Load and resample audio to 16kHz (required by wav2vec2)
        audio, sr = librosa.load(audio_path, sr=16000, mono=True)
        
        # Save as temporary WAV file
        temp_wav = audio_path.replace('.webm', '_converted.wav')
        sf.write(temp_wav, audio, 16000)
        
        # Analyze with the model
        res = audio_pipe(temp_wav)
        
        # Clean up temp file
        if os.path.exists(temp_wav):
            os.remove(temp_wav)
        
        if isinstance(res, list) and len(res) > 0:
            # Get top result
            top_result = res[0]
            label = str(top_result["label"]).title()
            score = float(top_result["score"])
            
            # If confidence is too low, check second best
            if score < 0.3 and len(res) > 1:
                label = str(res[1]["label"]).title()
                score = float(res[1]["score"])
            
            return label, score
        return "Neutral", 0.0
    except Exception as e:
        print(f"Audio analysis error: {e}")
        return "Neutral", 0.0

def train_models():
    if not os.path.exists(CSV_FILE) or os.path.getsize(CSV_FILE) == 0:
        return None, None
    df = pd.read_csv(CSV_FILE)
    if df.empty or len(df) < 3: 
        return None, None
    
    def combine_emotions(row):
        labels = [row["text_label"], row["image_label"], row["audio_label"]]
        return max(set(labels), key=labels.count)
    
    df["overall_emotion"] = df.apply(combine_emotions, axis=1)
    X = df[["text_score", "image_score", "audio_score"]]
    y = df["overall_emotion"]
    
    tree = DecisionTreeClassifier(max_depth=3, random_state=42)
    knn = KNeighborsClassifier(n_neighbors=min(3, len(df)))
    tree.fit(X, y)
    knn.fit(X, y)
    return tree, knn

def create_chart_base64(text_label, text_score, image_label, image_score, audio_label, audio_score):
    labels = ["Text", "Image", "Audio"]
    scores = [text_score, image_score, audio_score]
    emotions = [text_label, image_label, audio_label]
    colors = ['#667eea', '#764ba2', '#f093fb']
    
    fig, ax = plt.subplots(figsize=(10, 5), facecolor='white')
    bars = ax.bar(labels, scores, color=colors, alpha=0.8, edgecolor='white', linewidth=2)
    
    ax.set_ylim(0, 1.1)
    ax.set_ylabel("Confidence Score", fontsize=12, fontweight='bold', color='#333')
    ax.set_title("Emotion Detection Confidence", fontsize=14, fontweight='bold', color='#333', pad=20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#ccc')
    ax.spines['bottom'].set_color('#ccc')
    ax.tick_params(colors='#666', labelsize=10)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    for b, emo, sc in zip(bars, emotions, scores):
        height = b.get_height()
        ax.text(b.get_x() + b.get_width()/2, height/2, 
                f"{emo}", ha="center", va="center", 
                fontsize=11, fontweight='bold', color='white')
        ax.text(b.get_x() + b.get_width()/2, height + 0.03, 
                f"{sc:.1%}", ha="center", va="bottom",
                fontsize=10, fontweight='bold', color='#333')
    
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png", dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    buf.seek(0)
    
    return base64.b64encode(buf.read()).decode()

@app.get("/")
def read_root():
    return {"message": "Emotion Recognition API", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "models_loaded": True}

@app.post("/analyze")
async def analyze_emotion(
    text: str = Form(...),
    image: UploadFile = File(...),
    audio: UploadFile = File(...)
):
    try:
        # Analyze text
        t_label, t_score = analyze_text(text)
        
        # Analyze image
        img_bytes = await image.read()
        img = Image.open(io.BytesIO(img_bytes))
        i_label, i_score = analyze_image(img)
        
        # Analyze audio
        audio_bytes = await audio.read()
        audio_path = f"temp_audio_{int(time.time())}.wav"
        with open(audio_path, "wb") as f:
            f.write(audio_bytes)
        a_label, a_score = analyze_audio(audio_path)
        os.remove(audio_path)
        
        # Save results
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row = {
            "timestamp": ts,
            "text": text,
            "text_label": t_label,
            "text_score": round(t_score, 3),
            "image_label": i_label,
            "image_score": round(i_score, 3),
            "audio_label": a_label,
            "audio_score": round(a_score, 3)
        }
        
        df = pd.read_csv(CSV_FILE)
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)
        
        # Train ML models
        tree, knn = train_models()
        dt_pred = "N/A"
        knn_pred = "N/A"
        
        if tree and knn:
            sample = [[t_score, i_score, a_score]]
            dt_pred = tree.predict(sample)[0]
            knn_pred = knn.predict(sample)[0]
        
        # Create chart
        chart_base64 = create_chart_base64(t_label, t_score, i_label, i_score, a_label, a_score)
        
        return {
            "success": True,
            "timestamp": ts,
            "text": {
                "label": t_label,
                "score": round(t_score, 3)
            },
            "image": {
                "label": i_label,
                "score": round(i_score, 3)
            },
            "audio": {
                "label": a_label,
                "score": round(a_score, 3)
            },
            "ml_predictions": {
                "decision_tree": dt_pred,
                "knn": knn_pred
            },
            "chart": chart_base64,
            "total_records": len(df)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history")
def get_history(limit: int = 10):
    try:
        df = pd.read_csv(CSV_FILE)
        records = df.tail(limit).to_dict('records')
        return {"success": True, "records": records, "total": len(df)}
    except:
        return {"success": True, "records": [], "total": 0}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
