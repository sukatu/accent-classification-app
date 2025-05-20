import whisper
from transformers import pipeline

import torch

# Load Whisper base model for transcription
whisper_model = whisper.load_model("base")

# Use zero-shot-classification pipeline for accent classification
accent_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", framework="pt")

def classify_accent(audio_path):
    transcription = whisper_model.transcribe(audio_path)["text"]

    # Simulate accent prediction by inferring from the transcription (replace this logic as needed)
    classes = ["British English", "American English", "Indian English", "Nigerian English", "Australian English"]
    response = accent_classifier(transcription, candidate_labels=classes)

    top = response["labels"][0]
    score = response["scores"][0]
    return {
        "transcription": transcription,
        "accent": top,
        "confidence": round(score * 100, 2),
        "summary": f"The speaker appears to have a {top} accent with {round(score*100)}% confidence."
    }