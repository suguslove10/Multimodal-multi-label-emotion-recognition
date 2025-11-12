🎭 MULTIMODAL EMOTION RECOGNITION
==================================

AI-powered emotion analysis using text, facial expressions, and voice tone.

📋 REQUIREMENTS
---------------
- Python 3.10, 3.11, 3.12, or 3.13 (NOT 3.14)
- Webcam (for facial expression capture)
- Microphone (for voice recording)
- 2-3 GB free disk space (for AI models)
- Internet connection (first run only)

🚀 HOW TO RUN
-------------

FOR MAC/LINUX:
1. Open Terminal
2. Navigate to this folder
3. Run: ./run.sh

FOR WINDOWS:
1. Open Command Prompt or PowerShell
2. Navigate to this folder
3. Run: run.bat

⏱️ FIRST RUN
------------
- Takes 1-2 minutes to download AI models (~1-2 GB)
- Subsequent runs are much faster
- A web interface will open in your browser

🎯 HOW TO USE
-------------
1. Type how you're feeling in the text box
2. Capture or upload a photo (facial expression)
3. Record a short audio clip (5-10 seconds)
4. Click "Analyze My Emotions"
5. View results with confidence scores and ML predictions

📊 FEATURES
-----------
✓ Text emotion analysis
✓ Facial expression recognition
✓ Voice tone analysis
✓ Decision Tree classification
✓ K-Nearest Neighbors prediction
✓ Confidence visualization charts
✓ Export results to CSV
✓ Analysis history tracking

🔧 TROUBLESHOOTING
------------------
- If Python 3.14 error: Install Python 3.13 or lower
- If "command not found": Make sure Python is installed
- If models fail to load: Check internet connection
- If webcam/mic not working: Check browser permissions

📁 FILES
--------
- emotion_recognition.py : Main application code
- requirements.txt       : Python dependencies
- run.sh                 : Mac/Linux startup script
- run.bat                : Windows startup script
- emotion_results.csv    : Saved analysis results (created on first use)

💡 TIPS
-------
- Speak naturally for 5-10 seconds when recording
- Ensure good lighting for facial photos
- Be authentic in your text descriptions
- The more data you analyze, the better ML predictions become

🛠️ TECH STACK
--------------
- Gradio: Web interface
- Transformers: Deep learning models
- PyTorch: Neural network framework
- Scikit-learn: Machine learning algorithms
- Matplotlib: Data visualization
- Pandas: Data management
