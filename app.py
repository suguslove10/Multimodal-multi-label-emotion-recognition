import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
import io, time, os
from PIL import Image
from transformers import pipeline
import torch
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
import warnings
warnings.filterwarnings("ignore")

# Setup
CSV_FILE = "emotion_results.csv"
DEVICE = 0 if torch.cuda.is_available() else -1

if not os.path.exists(CSV_FILE):
    pd.DataFrame(columns=["timestamp","text","text_label","text_score",
                          "image_label","image_score","audio_label","audio_score"]).to_csv(CSV_FILE, index=False)

# Load Models
print("Loading AI models...")
text_pipe = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", device=DEVICE)
image_pipe = pipeline("image-classification", model="trpakov/vit-face-expression", top_k=5, device=DEVICE)
audio_pipe = pipeline("audio-classification", model="ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition", top_k=6, device=DEVICE)
print("✅ Models loaded")

def analyze_text(text):
    try:
        res = text_pipe(text)
        if isinstance(res, list): res = res[0]
        return str(res["label"]).title(), float(res["score"])
    except:
        return "Neutral", 0.0

def analyze_image(img):
    try:
        res = image_pipe(img)
        if isinstance(res, list) and len(res) > 0:
            return str(res[0]["label"]).title(), float(res[0]["score"])
        return "Neutral", 0.0
    except:
        return "Neutral", 0.0

def analyze_audio(aud_path):
    try:
        res = audio_pipe(aud_path)
        if isinstance(res, list) and len(res) > 0:
            return str(res[0]["label"]).title(), float(res[0]["score"])
        return "Neutral", 0.0
    except:
        return "Neutral", 0.0

def create_chart(text_label, text_score, image_label, image_score, audio_label, audio_score):
    labels = ["Text", "Image", "Audio"]
    scores = [text_score, image_score, audio_score]
    emotions = [text_label, image_label, audio_label]
    colors = ['#667eea', '#764ba2', '#f093fb']
    
    fig, ax = plt.subplots(figsize=(10, 5), facecolor='white')
    bars = ax.bar(labels, scores, color=colors, alpha=0.85, edgecolor='white', linewidth=3)
    
    ax.set_ylim(0, 1.1)
    ax.set_ylabel("Confidence Score", fontsize=13, fontweight='bold', color='#333')
    ax.set_title("Emotion Detection Confidence", fontsize=15, fontweight='bold', color='#333', pad=20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#ccc')
    ax.spines['bottom'].set_color('#ccc')
    ax.tick_params(colors='#666', labelsize=11)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    for b, emo, sc in zip(bars, emotions, scores):
        height = b.get_height()
        ax.text(b.get_x() + b.get_width()/2, height/2, 
                f"{emo}", ha="center", va="center", 
                fontsize=12, fontweight='bold', color='white')
        ax.text(b.get_x() + b.get_width()/2, height + 0.03, 
                f"{sc:.1%}", ha="center", va="bottom",
                fontsize=11, fontweight='bold', color='#333')
    
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png", dpi=200, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf)

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

def process_all(user_text, user_image, user_audio):
    if not user_text or user_image is None or user_audio is None:
        return "⚠️ Please provide all three inputs", None, None, None
    
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    t_label, t_score = analyze_text(user_text)
    i_label, i_score = analyze_image(user_image)
    a_label, a_score = analyze_audio(user_audio)
    
    row = {
        "timestamp": ts,
        "text": user_text,
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
    
    chart = create_chart(t_label, t_score, i_label, i_score, a_label, a_score)
    
    tree, knn = train_models()
    dt_pred = "N/A"
    knn_pred = "N/A"
    
    if tree and knn:
        sample = [[t_score, i_score, a_score]]
        dt_pred = tree.predict(sample)[0]
        knn_pred = knn.predict(sample)[0]
    
    summary = f"""
# 🎭 Emotion Analysis Results

**📅 Time:** {ts}

---

### 📊 Detection Results

| Modality | Emotion | Confidence |
|----------|---------|------------|
| 📝 **Text** | **{t_label}** | {t_score:.1%} |
| 📷 **Image** | **{i_label}** | {i_score:.1%} |
| 🎤 **Audio** | **{a_label}** | {a_score:.1%} |

---

### 🤖 Machine Learning Predictions

- **Decision Tree:** `{dt_pred}`
- **K-Nearest Neighbors:** `{knn_pred}`

---

✅ **Analysis saved** • Total records: **{len(df)}**
"""
    
    history_df = df.tail(10).reset_index(drop=True)
    return summary, chart, CSV_FILE, history_df

# Gradio Interface
with gr.Blocks(theme=gr.themes.Soft(), title="AI Emotion Recognition") as demo:
    gr.Markdown("""
    # 🎭 AI-Powered Emotion Recognition
    ### Advanced multimodal emotion analysis using Deep Learning
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("## 📥 Input Data")
            
            txt = gr.Textbox(
                label="💭 How are you feeling?",
                placeholder="Describe your emotions...",
                lines=4
            )
            
            img = gr.Image(
                label="📸 Facial Expression",
                sources=["webcam", "upload"],
                type="pil"
            )
            
            aud = gr.Audio(
                label="🎙️ Voice Recording",
                sources=["microphone", "upload"],
                type="filepath"
            )
            
            btn = gr.Button("🚀 Analyze Emotions", variant="primary", size="lg")
            
            gr.Markdown("""
            **💡 Tips:**
            - Speak naturally for 5-10 seconds
            - Ensure good lighting for photos
            - Be authentic in your text
            """)
        
        with gr.Column(scale=1):
            gr.Markdown("## 📊 Analysis Results")
            
            out_md = gr.Markdown("*Awaiting input...*")
            out_chart = gr.Image(label="📈 Confidence Chart")
            
            with gr.Accordion("📋 Recent History", open=False):
                out_df = gr.Dataframe(label="Last 10 Analyses")
            
            with gr.Accordion("💾 Export Data", open=False):
                out_csv = gr.File(label="Download CSV")
    
    btn.click(
        process_all,
        inputs=[txt, img, aud],
        outputs=[out_md, out_chart, out_csv, out_df]
    )
    
    gr.Markdown("""
    ---
    **Powered by:** Hugging Face Transformers • PyTorch • Scikit-learn • Gradio
    """)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", share=True)
