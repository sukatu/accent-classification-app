import os
import tempfile
import streamlit as st
import requests
from utils.accent_model import classify_accent
import torch
import asyncio

# Set up the event loop for Streamlit
if not asyncio.get_event_loop().is_running():
    asyncio.set_event_loop(asyncio.new_event_loop())

# Initialize PyTorch
@st.cache_resource
def init_torch():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    return device

def has_audio_stream(file_path):
    import subprocess
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=codec_type", "-of", "default=noprint_wrappers=1:nokey=1", file_path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        st.info(f"ffprobe output: {result.stdout}")  # For debugging
        return "audio" in result.stdout
    except Exception:
        return False

def process_video(video_file):
    try:
        # Create a temporary file to store the video
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
            tmp_path = tmp_file.name
            tmp_file.write(video_file.read())
        
        # Get file extension
        file_suffix = os.path.splitext(video_file.name)[1]
        
        # Play the video
        st.video(tmp_path)
        
        # Clean up
        os.unlink(tmp_path)
        
        return True
        
    except Exception as e:
        st.error(f"Error processing video: {str(e)}")
        if 'tmp_path' in locals():
            os.unlink(tmp_path)
        return None

# Main app
def main():
    st.title("Accent Classification App By (Issa Sukatu Abdullahi sukaissa@gmail.com)")
    
    # Initialize PyTorch
    device = init_torch()
    st.write(f"Using device: {device}")
    
    uploaded_file = st.file_uploader("Upload an audio file (.wav, .mp3, .mp4)", type=["wav", "mp3", "mp4"])
    video_url = st.text_input("Or enter a public video URL (e.g., direct MP4 link):")

    tmp_path = None

    if uploaded_file is not None:
        file_suffix = os.path.splitext(uploaded_file.name)[1].lower()
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_suffix) as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name
        st.success(f"Temporary file saved at: {tmp_path}")
        if file_suffix == ".mp4":
            if process_video(uploaded_file):
                if not has_audio_stream(tmp_path):
                    st.error("This video file does not contain an audio stream.")
                    tmp_path = None
        else:
            st.audio(tmp_path, format=f'audio/{file_suffix[1:]}')

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
                    if process_video(uploaded_file):
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

if __name__ == "__main__":
    main()