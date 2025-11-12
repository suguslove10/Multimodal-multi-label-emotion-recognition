# === Multimodal Emotion Recognition (Text + Webcam + Microphone) + Decision Tree + KNN ===
# ✅ Works with Gradio >= 4.44 and Transformers >= 4.44!

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

# -------------------------------
# SETUP
# -------------------------------
CSV_FILE = "emotion_results.csv"
DEVICE = 0 if torch.cuda.is_available() else -1

# Create CSV if not exists
if not os.path.exists(CSV_FILE):
    pd.DataFrame(columns=["timestamp","text","text_label","text_score",
                          "image_label","image_score","audio_label","audio_score"]).to_csv(CSV_FILE, index=False)

# -------------------------------
# Load Models
# -------------------------------
print("Loading models (please wait 1–2 mins)...")
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
print("✅ Models loaded successfully.")

# -------------------------------
# Helper Functions
# -------------------------------
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

def save_result(row):
    df = pd.read_csv(CSV_FILE)
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

def create_chart(text_label, text_score, image_label, image_score, audio_label, audio_score):
    labels = ["Text\nAnalysis", "Facial\nExpression", "Voice\nTone"]
    scores = [text_score, image_score, audio_score]
    emotions = [text_label, image_label, audio_label]
    
    # Modern color palette
    colors = ['#667eea', '#764ba2', '#f093fb']
    
    fig, ax = plt.subplots(figsize=(10, 5), facecolor='white')
    bars = ax.bar(labels, scores, color=colors, alpha=0.8, edgecolor='white', linewidth=2)
    
    # Styling
    ax.set_ylim(0, 1.1)
    ax.set_ylabel("Confidence Score", fontsize=12, fontweight='bold', color='#333')
    ax.set_title("Emotion Detection Confidence by Modality", 
                 fontsize=14, fontweight='bold', color='#333', pad=20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#ccc')
    ax.spines['bottom'].set_color('#ccc')
    ax.tick_params(colors='#666', labelsize=10)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    # Add value labels on bars
    for b, emo, sc in zip(bars, emotions, scores):
        height = b.get_height()
        # Emotion label inside bar
        ax.text(b.get_x() + b.get_width()/2, height/2, 
                f"{emo}", ha="center", va="center", 
                fontsize=11, fontweight='bold', color='white')
        # Score above bar
        ax.text(b.get_x() + b.get_width()/2, height + 0.03, 
                f"{sc:.1%}", ha="center", va="bottom",
                fontsize=10, fontweight='bold', color='#333')
    
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png", dpi=200, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf)

# -------------------------------
# Decision Tree + KNN Predictors
# -------------------------------
def train_models():
    if not os.path.exists(CSV_FILE) or os.path.getsize(CSV_FILE) == 0:
        return None, None
    df = pd.read_csv(CSV_FILE)
    if df.empty: return None, None
    
    def combine_emotions(row):
        labels = [row["text_label"], row["image_label"], row["audio_label"]]
        return max(set(labels), key=labels.count)
    
    df["overall_emotion"] = df.apply(combine_emotions, axis=1)
    X = df[["text_score", "image_score", "audio_score"]]
    y = df["overall_emotion"]
    
    tree = DecisionTreeClassifier(max_depth=3, random_state=42)
    knn = KNeighborsClassifier(n_neighbors=3)
    tree.fit(X, y)
    knn.fit(X, y)
    return tree, knn

# -------------------------------
# Main Function
# -------------------------------
def process_all(user_text, user_image, user_audio):
    if not user_text or user_image is None or user_audio is None:
        return ("⚠️ Please provide all three inputs: text, photo, and audio.",
                None, None, None)
    
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
    save_result(row)
    
    chart = create_chart(t_label, t_score, i_label, i_score, a_label, a_score)
    
    tree, knn = train_models()
    dt_pred, knn_pred = "N/A", "N/A"
    if tree and knn:
        sample = [[t_score, i_score, a_score]]
        dt_pred = tree.predict(sample)[0]
        knn_pred = knn.predict(sample)[0]
    
    summary = f"""
<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 15px; color: white;'>
<h2 style='margin: 0 0 1rem 0; font-size: 1.8rem;'>🧠 Emotion Analysis Complete</h2>
<p style='opacity: 0.9; margin: 0;'>📅 {ts}</p>
</div>

<div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin: 1.5rem 0;'>
<div style='background: #f8f9fa; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #667eea;'>
<h3 style='margin: 0 0 0.5rem 0; color: #667eea;'>📝 Text Analysis</h3>
<p style='font-size: 1.5rem; font-weight: bold; margin: 0; color: #333;'>{t_label}</p>
<p style='color: #666; margin: 0.5rem 0 0 0;'>Confidence: {t_score:.1%}</p>
</div>

<div style='background: #f8f9fa; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #764ba2;'>
<h3 style='margin: 0 0 0.5rem 0; color: #764ba2;'>📷 Facial Expression</h3>
<p style='font-size: 1.5rem; font-weight: bold; margin: 0; color: #333;'>{i_label}</p>
<p style='color: #666; margin: 0.5rem 0 0 0;'>Confidence: {i_score:.1%}</p>
</div>

<div style='background: #f8f9fa; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #f093fb;'>
<h3 style='margin: 0 0 0.5rem 0; color: #f093fb;'>🎤 Voice Tone</h3>
<p style='font-size: 1.5rem; font-weight: bold; margin: 0; color: #333;'>{a_label}</p>
<p style='color: #666; margin: 0.5rem 0 0 0;'>Confidence: {a_score:.1%}</p>
</div>
</div>

<div style='background: #fff3cd; padding: 1.5rem; border-radius: 12px; margin: 1.5rem 0; border: 2px solid #ffc107;'>
<h3 style='margin: 0 0 1rem 0; color: #856404;'>🤖 Machine Learning Predictions</h3>
<div style='display: flex; gap: 2rem; justify-content: space-around;'>
<div style='text-align: center;'>
<p style='margin: 0; color: #666; font-size: 0.9rem;'>Decision Tree</p>
<p style='font-size: 1.8rem; font-weight: bold; margin: 0.5rem 0 0 0; color: #856404;'>{dt_pred}</p>
</div>
<div style='text-align: center;'>
<p style='margin: 0; color: #666; font-size: 0.9rem;'>K-Nearest Neighbors</p>
<p style='font-size: 1.8rem; font-weight: bold; margin: 0.5rem 0 0 0; color: #856404;'>{knn_pred}</p>
</div>
</div>
</div>

<div style='text-align: center; padding: 1rem; background: #d4edda; border-radius: 10px; color: #155724;'>
✅ <strong>Analysis saved successfully</strong> • Total records: {len(pd.read_csv(CSV_FILE))}
</div>
"""
    
    df = pd.read_csv(CSV_FILE).tail(10).reset_index(drop=True)
    return summary, chart, CSV_FILE, df

# -------------------------------
# Gradio UI - Professional Design
# -------------------------------
css = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

.gradio-container {
    font-family: 'Inter', sans-serif !important;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
}

#main-container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 2rem;
}

#header {
    text-align: center;
    padding: 2rem 0;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    margin-bottom: 2rem;
    box-shadow: 0 10px 40px rgba(0,0,0,0.1);
}

#header h1 {
    font-size: 2.5rem;
    font-weight: 700;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}

#header p {
    color: #666;
    font-size: 1.1rem;
    margin: 0.5rem 0;
}

.input-card, .output-card {
    background: rgba(255, 255, 255, 0.98);
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    backdrop-filter: blur(10px);
}

.section-title {
    font-size: 1.3rem;
    font-weight: 600;
    color: #333;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 3px solid #667eea;
}

.gr-button-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 32px !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
    transition: all 0.3s ease !important;
}

.gr-button-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6) !important;
}

.gr-input, .gr-box {
    border-radius: 10px !important;
    border: 2px solid #e0e0e0 !important;
}

.gr-input:focus, .gr-box:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
}

#results-area {
    min-height: 400px;
}

.stats-badge {
    display: inline-block;
    padding: 0.5rem 1rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 20px;
    font-weight: 600;
    margin: 0.25rem;
}

footer {
    text-align: center;
    padding: 2rem;
    color: white;
    font-size: 0.9rem;
}
"""

with gr.Blocks(theme=gr.themes.Soft(), css=css, title="Emotion Recognition AI") as demo:
    with gr.Column(elem_id="main-container"):
        # Header
        with gr.Column(elem_id="header"):
            gr.Markdown("# 🎭 AI-Powered Multimodal Emotion Recognition")
            gr.Markdown("Advanced emotion analysis using Deep Learning, Decision Trees & KNN Classification")
            gr.Markdown("📝 Text Analysis • 📷 Facial Expression • 🎤 Voice Tone Recognition")
        
        # Main Content
        with gr.Row(equal_height=True):
            # Left Panel - Inputs
            with gr.Column(scale=1, elem_classes="input-card"):
                gr.Markdown("<div class='section-title'>📥 Input Data</div>")
                
                txt = gr.Textbox(
                    label="💭 How are you feeling?", 
                    placeholder="Express your emotions in words...",
                    lines=3,
                    info="Describe your current emotional state"
                )
                
                img = gr.Image(
                    label="📸 Facial Expression", 
                    sources=["webcam", "upload"],
                    type="pil",
                    height=300,
                    info="Capture or upload your photo"
                )
                
                aud = gr.Audio(
                    label="🎙️ Voice Recording", 
                    sources=["microphone"],
                    type="filepath",
                    info="Record a short audio clip (5-10 seconds)"
                )
                
                btn = gr.Button(
                    "🚀 Analyze My Emotions",
                    variant="primary",
                    size="lg"
                )
                
                gr.Markdown("""
                <div style='margin-top: 1rem; padding: 1rem; background: #f8f9fa; border-radius: 10px; font-size: 0.9rem;'>
                <strong>💡 Tips:</strong><br>
                • Speak naturally for 5-10 seconds<br>
                • Ensure good lighting for photos<br>
                • Be authentic in your text input
                </div>
                """)
            
            # Right Panel - Results
            with gr.Column(scale=1, elem_classes="output-card"):
                gr.Markdown("<div class='section-title'>📊 Analysis Results</div>")
                
                out_md = gr.Markdown(
                    """
                    <div style='text-align: center; padding: 3rem; color: #999;'>
                    <h3>👈 Ready to analyze</h3>
                    <p>Provide all three inputs and click the analyze button</p>
                    </div>
                    """,
                    elem_id="results-area"
                )
                
                out_chart = gr.Image(
                    label="📈 Confidence Visualization",
                    show_label=True
                )
                
                with gr.Accordion("📋 Recent Analysis History", open=False):
                    out_df = gr.Dataframe(
                        label="Last 10 Predictions",
                        interactive=False,
                        wrap=True
                    )
                
                with gr.Accordion("💾 Export Data", open=False):
                    out_csv = gr.File(label="Download Complete Dataset (CSV)")
        
        # Footer
        gr.Markdown("""
        <footer>
        <strong>Powered by:</strong> Hugging Face Transformers • PyTorch • Scikit-learn • Gradio<br>
        <em>Real-time emotion recognition with state-of-the-art AI models</em>
        </footer>
        """)
    
    # Event Handler
    btn.click(
        process_all,
        inputs=[txt, img, aud],
        outputs=[out_md, out_chart, out_csv, out_df]
    )

demo.launch(share=True, server_name="0.0.0.0")
