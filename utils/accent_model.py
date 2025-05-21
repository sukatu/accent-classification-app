import whisper
from transformers import pipeline

import torch

# Load Whisper base model for transcription
whisper_model = whisper.load_model("base")

# Dummy accent classifier using huggingface sentiment pipeline for now
# You can replace this with a custom fine-tuned accent model
accent_classifier = pipeline(
    "zero-shot-classification",
    model="typeform/distilbert-base-uncased-mnli",  # ✅ Lighter model
    framework="pt"
)
def classify_accent(text):
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    result = classifier(text, candidate_labels=["American", "British", "Australian", "Indian", "Nigerian"])
    return result['labels'][0], round(result['scores'][0] * 100, 2), text

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
