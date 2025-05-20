# English Accent Classifier (Streamlit App)

## 🚀 What It Does
Takes a public video URL (MP4/Loom), extracts the audio, transcribes speech, and detects English accent (British, American, etc.).

## 🔧 Features
- Whisper model for transcription
- Hugging Face transformer for accent classification
- Simple Streamlit UI

## ▶️ Running Locally
```bash
git clone https://github.com/issasuka/english-accent-classifier.git
cd english-accent-classifier
pip install -r requirements.txt
streamlit run app.py
