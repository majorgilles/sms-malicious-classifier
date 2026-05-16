# LEARNINGS.md

## Issue 3: Fine-tuning DistilBERT

These notes capture learning from implementing GitHub issue #3:
fine-tuning DistilBERT on the SMS dataset.

## Hugging Face and DistilBERT

This project uses the Hugging Face ecosystem:

- `transformers` for tokenizer/model loading and training helpers
- `datasets` for model-ready dataset objects
- `evaluate` for validation metrics
- PyTorch as the backend deep learning framework

`distilbert-base-uncased` is a pretrained model checkpoint. It already knows a
lot about English from pretraining, so this project does not train a language
model from scratch. Fine-tuning adapts the pretrained model to the specific
task: classifying SMS messages as `benign` or `malicious`.

When loading `AutoModelForSequenceClassification` from `distilbert-base-uncased`,
Hugging Face warns that some weights are unexpected and some are missing. This
is expected:

- the old pretraining head is not used for SMS classification
- a new two-label classification head is initialized
- fine-tuning trains that new classification head for this project

## Labels

The human-readable labels are:

```text
benign
malicious
```

The model needs numeric labels:

```python
LABEL_TO_ID = {
    "benign": 0,
    "malicious": 1,
}

ID_TO_LABEL = {
    0: "benign",
    1: "malicious",
}
```

Keeping this mapping consistent matters across training, evaluation, and
prediction.

The Hugging Face `Trainer` expects the numeric target column to be named:

```text
labels
```

The readable string column:

```text
label
```

is useful for humans, but it cannot be turned into a training tensor.

## Tokenization

DistilBERT cannot process raw strings directly. The tokenizer converts SMS text
into numeric inputs.

A raw row looks like:

```python
{
    "message": "Free prize now!",
    "label": "malicious",
    "labels": 1,
}
```

A tokenized row includes model inputs:

```python
{
    "message": "Free prize now!",
    "label": "malicious",
    "labels": 1,
    "input_ids": [101, 2489, 3396, 2085, 999, 102],
    "attention_mask": [1, 1, 1, 1, 1, 1],
}
```

Important fields:

- `input_ids`: token IDs from DistilBERT's vocabulary
- `attention_mask`: marks real tokens with `1` and padding with `0`
- `labels`: numeric correct answer used for training loss

Example:

```python
[101, 7592, 102]
```

decodes roughly to:

```text
[CLS] hello [SEP]
```

The tokenizer uses a max length of `128`, which is appropriate for short SMS
messages and keeps training fast.

## Data collator and padding

SMS messages tokenize to different lengths. A training batch must become a
rectangular tensor, so examples in the same batch need equal length.

`DataCollatorWithPadding` pads dynamically per batch. This is better than
padding every message to `MAX_LENGTH=128` upfront because short messages only
get as much padding as needed for their current batch.

## Why remove `message` and `label` before training?

The first training attempt failed with an error about the `label` feature:

```text
Unable to create tensor...
Perhaps your features (`label` in this case) have excessive nesting...
```

The cause was that the tokenized dataset still contained:

```python
"label": "malicious"
```

The data collator tried to turn every batch field into tensors, but strings
cannot become model tensors.

The fix was to remove human-readable columns before training:

```python
columns_to_remove = ["message", "label"]

train_features = tokenized_train_dataset.remove_columns(columns_to_remove)
validation_features = tokenized_validation_dataset.remove_columns(columns_to_remove)
```

After cleanup, the model-ready dataset contains numeric/model fields:

```python
{
    "labels": 1,
    "input_ids": [...],
    "token_type_ids": [...],
    "attention_mask": [...],
}
```

## Trainer inputs

`Trainer` receives the tokenized datasets, not raw pandas dataframes and not raw
text datasets.

This is because Hugging Face's DistilBERT model expects named inputs like:

```text
input_ids
attention_mask
labels
```

More precisely:

- the DistilBERT architecture needs token IDs and attention information
- Hugging Face names those inputs `input_ids` and `attention_mask`
- `Trainer` passes `labels` so the model can compute training loss

## Device and CUDA

The notebook checks whether CUDA is available:

```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
```

`model.to(device)` moves the model weights to the selected device.

- `cuda`: NVIDIA GPU through PyTorch/CUDA
- `cpu`: regular processor fallback

Hugging Face `Trainer` handles moving training batches to the same device as the
model.

Running a game while training is a bad idea because both workloads compete for:

- GPU compute
- VRAM
- power and thermal headroom

## Metrics

The project uses Hugging Face `evaluate` for validation metrics.

Accuracy answers:

```text
What fraction of all predictions were correct?
```

F1 combines precision and recall.

For this project, the most important class is `malicious`.

For the malicious class:

```text
precision = when the model says "malicious", how often it is right
recall = of all truly malicious messages, how many the model catches
```

F1 combines them:

```text
F1 = 2 * (precision * recall) / (precision + recall)
```

The notebook uses:

```python
average="binary"
pos_label=1
```

This means:

- compute F1 for one selected class
- select label `1`
- in this project, label `1` means `malicious`

## Logits and predictions

The model outputs raw scores called logits.

Example logits for one message:

```python
[-1.2, 2.4]
```

Interpretation:

```text
score for label 0 = -1.2
score for label 1 =  2.4
```

The larger score is the class the model currently favors. These are raw scores,
not probabilities.

`np.argmax(logits, axis=-1)` returns the index of the highest score, not the
score itself.

Example:

```python
[-1.2, 2.4] -> 1
```

That predicts label `1`, which means `malicious`.

Softmax can convert logits into probabilities if needed later for confidence
scores.

## Training loss vs validation loss

Training loss measures how wrong the model is on examples it is allowed to learn
from.

Validation loss measures how wrong the model is on held-out examples used only
to check progress.

In this run:

```text
Epoch    Training Loss    Validation Loss    Accuracy    F1
1        0.070212         0.058010           0.987455    0.951724
2        0.023470         0.059383           0.987455    0.953020
```

Training loss dropped from about `0.07` to `0.02`, meaning the model fit the
training data better.

Validation loss stayed roughly flat and slightly worsened. That suggests most
useful learning happened by epoch 1, while epoch 2 mostly improved fit on the
training data. This is not alarming because validation accuracy and F1 stayed
strong.

## Why only two epochs?

Fine-tuning is not training from scratch. DistilBERT already has general English
language knowledge. The SMS dataset is small, so a few passes are usually enough
to adapt the classifier head.

Using too many epochs could overfit, meaning the model memorizes training
examples instead of learning patterns that generalize.

For issue #3, two epochs are enough to prove the fine-tuning pipeline works.
Issue #4 will evaluate the saved model more carefully on the test set.

## Saved model artifacts

The trained model and tokenizer are saved to:

```text
models/distilbert-sms/
```

Generated files include:

```text
config.json
model.safetensors
tokenizer.json
tokenizer_config.json
training_args.bin
```

These files are generated artifacts and should not be committed to Git. The
repository should commit code and notebooks, while `.gitignore` keeps model
artifacts local.

## PyCharm and uv notes

The project uses a `src/` layout:

```text
src/sms_classifier/
```

PyCharm should mark `src/` as a Sources Root.

The project also uses a `.venv` created by `uv`. PyCharm should use:

```text
.venv/Scripts/python.exe
```

as the interpreter, while `.venv/` itself should be marked as Excluded in the
project tree. This lets PyCharm index installed packages correctly for import
suggestions without treating the virtual environment as project source code.

## Issue 4: Safety-aware evaluation

- Use the held-out test set for final evaluation because validation data can
  influence model selection.
- Load the saved model/tokenizer for evaluation; do not retrain in the eval
  notebook.
- Reuse shared label mappings so `benign = 0` and `malicious = 1` stay
  consistent.
- `Trainer.predict()` is useful for evaluation too: it handles batching,
  padding, device placement, and output collection.
- `TrainingArguments` is the `Trainer` runtime config even outside training.
- Accuracy is not enough for this task. Malicious recall and false negatives are
  the safety-critical signals.
- The confusion matrix makes error counts concrete, especially malicious
  messages predicted as benign.
- Saved metrics and plots may still be ignored by `.gitignore` unless tracking
  is intentionally enabled.
- Treat the SMS spam dataset as a proxy, not proof of production readiness.
- Before finalizing notebooks, remove duplicate/debug cells and rerun from a
  clean kernel.
