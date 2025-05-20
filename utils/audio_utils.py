import os
import requests
import uuid
import subprocess

def download_video(url):
    try:
        filename = f"temp_{uuid.uuid4().hex}.mp4"
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(filename, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return filename
    except Exception as e:
        print("Download failed:", e)
        return None

def extract_audio(video_path):
    audio_path = video_path.replace(".mp4", ".wav")
    command = ["ffmpeg", "-i", video_path, "-q:a", "0", "-map", "a", audio_path, "-y"]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    return audio_path
