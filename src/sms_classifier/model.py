from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    PreTrainedModel,
    PreTrainedTokenizerBase,
)

from sms_classifier.labels import ID_TO_LABEL, LABEL_TO_ID

MODEL_NAME = "distilbert-base-uncased"
MAX_LENGTH = 128


def load_tokenizer() -> PreTrainedTokenizerBase:
    return AutoTokenizer.from_pretrained(MODEL_NAME)


def load_sequence_classifier() -> PreTrainedModel:
    """Loads pretrained DistilBERT weights and adapts it for sequence classification.

    “Sequence” here means one whole SMS message.
    """

    return AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=2,  # 0 and 1, benign and malicious
        id2label=ID_TO_LABEL,
        label2id=LABEL_TO_ID,
    )
