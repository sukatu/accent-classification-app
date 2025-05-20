import streamlit as st
import whisper
import tempfile
import os
import requests
from moviepy.editor import VideoFileClip
from transformers import pipeline

# Title
st.title("English Accent Classifier Tool")
st.markdown("""
Paste a public video URL (e.g., Loom or direct MP4). The app will:
1. Download and extract audio
2. Transcribe and classify the speaker's English accent
3. Display confidence score
""")

# Input URL
video_url = st.text_input("Enter public video URL (must be direct link to MP4 or similar)")

# Load models
@st.cache_resource
def load_whisper():
    return whisper.load_model("base")

@st.cache_resource
def load_classifier():
    return pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Helper to download video
def download_video(url):
    temp_video = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    response = requests.get(url, stream=True)
    with open(temp_video.name, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return temp_video.name

# Extract audio from video
def extract_audio(video_path):
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(temp_audio.name, codec='pcm_s16le')
    return temp_audio.name

# Main logic
if st.button("Analyze") and video_url:
    with st.spinner("Downloading and processing video..."):
        video_file = download_video(video_url)
        audio_file = extract_audio(video_file)

        whisper_model = load_whisper()
        transcription = whisper_model.transcribe(audio_file)["text"]

        accent_labels = ["American", "British", "Australian", "Indian", "Nigerian"]
        classifier = load_classifier()
        result = classifier(transcription, candidate_labels=accent_labels)

        os.remove(video_file)
        os.remove(audio_file)

    st.subheader("Results")
    st.write(f"**Transcript:** {transcription}")
    st.write(f"**Predicted Accent:** {result['labels'][0]}")
    st.write(f"**Confidence Score:** {round(result['scores'][0] * 100, 2)}%")
    st.success("Analysis complete.")