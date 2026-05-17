from pathlib import Path

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from sms_classifier.labels import ID_TO_LABEL

DEFAULT_MODEL_DIR = Path("models/distilbert-sms")


def predict_message(
    message: str,
    model_dir: str | Path = DEFAULT_MODEL_DIR,
) -> tuple[str, float]:
    """Return the predicted label and confidence for one SMS message."""
    cleaned_message = message.strip()
    if not cleaned_message:
        raise ValueError("Message text must not be empty.")

    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForSequenceClassification.from_pretrained(model_dir)
    model.eval()

    inputs = tokenizer(
        cleaned_message,
        return_tensors="pt",
        truncation=True,
        max_length=128,
    )

    with torch.no_grad():
        outputs = model(**inputs)

    probabilities = torch.softmax(outputs.logits, dim=-1)
    confidence, predicted_id = torch.max(probabilities, dim=-1)
    label = ID_TO_LABEL[int(predicted_id.item())]

    return label, float(confidence.item())
