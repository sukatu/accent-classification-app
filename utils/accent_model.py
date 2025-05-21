import whisper
from transformers import pipeline

import torch

# Load Whisper base model for transcription
whisper_model = whisper.load_model("base")

# Dummy accent classifier using huggingface sentiment pipeline for now
# You can replace this with a custom fine-tuned accent model
accent_classifier = pipeline("text-classification", model="facebook/bart-large-mnli", framework="pt")

def classify_accent(audio_path):
    transcription = whisper_model.transcribe(audio_path)["text"]

    # Simulate accent prediction by inferring from the transcription (replace this logic as needed)
    classes = ["British English", "American English", "Indian English", "Nigerian English", "Australian English"]
    response = accent_classifier(transcription, candidate_labels=classes)

    top = response[0]
    return {
        "transcription": transcription,
        "accent": top["label"],
        "confidence": round(top["score"] * 100, 2),
        "summary": f"The speaker appears to have a {top['label']} accent with {round(top['score']*100)}% confidence."
    }
