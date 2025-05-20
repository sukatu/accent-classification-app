import os
import tempfile
import streamlit as st
import requests
from utils.accent_model import classify_accent

st.title("Accent Classification App By (Issa Sukatu Abdullahi sukaissa@gmail.com)")

uploaded_file = st.file_uploader("Upload an audio file (.wav, .mp3, .mp4)", type=["wav", "mp3", "mp4"])
video_url = st.text_input("Or enter a public video URL (e.g., direct MP4 link):")

tmp_path = None

def has_audio_stream(file_path):
    import subprocess
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=codec_type", "-of", "default=noprint_wrappers=1:nokey=1", file_path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        st.info(f"ffprobe output: {result.stdout}")
        return "audio" in result.stdout
    except Exception:
        return False

if uploaded_file is not None:
    file_suffix = os.path.splitext(uploaded_file.name)[1].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_suffix) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name
    st.success(f"Temporary file saved at: {tmp_path}")
    if file_suffix == ".mp4":
        st.video(tmp_path)
        if not has_audio_stream(tmp_path):
            st.error("This video file does not contain an audio stream. Please upload a video with recorded audio (e.g., speech or music).")
            tmp_path = None
    else:
        st.audio(tmp_path, format=f'audio/{file_suffix[1:]}")

elif video_url:
    try:
        file_suffix = os.path.splitext(video_url)[1].lower()
        if file_suffix not in [".mp4", ".wav", ".mp3"]:
            st.error("URL must point directly to a .mp4, .wav, or .mp3 file.")
        else:
            with tempfile.NamedTemporaryFile(delete=False, suffix=file_suffix) as tmp:
                response = requests.get(video_url, stream=True)
                for chunk in response.iter_content(chunk_size=8192):
                    tmp.write(chunk)
                tmp_path = tmp.name
            st.success(f"Downloaded file saved at: {tmp_path}")
            if file_suffix == ".mp4":
                st.video(tmp_path)
                if not has_audio_stream(tmp_path):
                    st.error("This video file does not contain an audio stream.")
                    tmp_path = None
            else:
                st.audio(tmp_path, format=f'audio/{file_suffix[1:]}')
    except Exception as e:
        st.error(f"Failed to download or preview file: {e}")

if tmp_path:
    try:
        transcript = classify_accent(tmp_path)
        st.subheader("Transcription:")
        st.write(transcript)
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)