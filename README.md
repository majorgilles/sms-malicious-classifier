# SMS Malicious Message Classifier

A small NLP portfolio project that classifies SMS messages as **malicious** or
**benign** with a fine-tuned DistilBERT model.

The project demonstrates an end-to-end machine-learning workflow:

1. explore and split a public SMS dataset,
2. fine-tune `distilbert-base-uncased`,
3. evaluate the saved model with safety-aware metrics, and
4. run one-message predictions from the command line.

> **Important limitation:** this first version uses the public UCI SMS
> Spam Collection as a practical proxy for malicious SMS detection. In plain
> language, the model has mostly learned the difference between older
> **spam/ham** examples, not the full range of modern smishing, phishing,
> bank-fraud, delivery-scam, or account-takeover messages. Treat it as a
> learning project and demo, not as a production security detector.

## Results summary

The latest evaluation is saved in [`reports/metrics.json`](reports/metrics.json)
and was produced by `notebooks/03_evaluate_and_demo.ipynb` on the held-out test
split.

| Metric | Value |
| --- | ---: |
| Accuracy | 98.92% |
| Malicious precision | 97.24% |
| Malicious recall | 94.63% |
| Malicious F1 | 95.92% |

Confusion matrix on 1,115 test messages:

| True label | Predicted benign | Predicted malicious |
| --- | ---: | ---: |
| benign | 962 | 4 |
| malicious | 8 | 141 |

The most important portfolio takeaway is malicious-message recall: the model
caught 141 of 149 spam-like malicious messages in the test split, while missing
8. Because the dataset is only a proxy, these numbers should not be interpreted
as real-world smishing detection performance.

## Quick start

### 1. Clone and install

```bash
git clone https://github.com/majorgilles/sms-malicious-classifier.git
cd sms-malicious-classifier
uv sync
```

### 2. Register the Jupyter kernel

```bash
uv run python -m ipykernel install --user --name sms-malicious-classifier --display-name "SMS Malicious Classifier"
```

### 3. Launch notebooks

```bash
uv run jupyter lab
```

Run the notebooks in order:

1. [`notebooks/01_data_exploration.ipynb`](notebooks/01_data_exploration.ipynb)
   - loads the SMS spam/ham data,
   - maps `ham` to `benign` and `spam` to `malicious`,
   - inspects class balance and examples,
   - saves train/validation/test CSV files under `data/processed/`.
2. [`notebooks/02_train_distilbert.ipynb`](notebooks/02_train_distilbert.ipynb)
   - tokenizes messages with the DistilBERT tokenizer,
   - fine-tunes `distilbert-base-uncased`,
   - saves the model and tokenizer to `models/distilbert-sms/`.
3. [`notebooks/03_evaluate_and_demo.ipynb`](notebooks/03_evaluate_and_demo.ipynb)
   - loads the saved model,
   - evaluates the held-out test split,
   - saves metrics to `reports/metrics.json`,
   - saves the confusion-matrix figure to `reports/figures/`,
   - includes example predictions and limitations.

### 4. Optional: verify GPU support

Training can run on CPU, but it is much faster with CUDA.

```bash
uv run python -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU only')"
```

## CLI demo

After running the training notebook, classify one SMS message with:

```bash
uv run python scripts/predict.py "Hey, are we still meeting at 6?"
```

Sample output:

```text
label: benign
confidence: 99.75%
```

Another example using a spam-style message from the project dataset:

```bash
uv run python scripts/predict.py "WIN: We have a winner! Mr. T. Foley won an iPod! More exciting prizes soon, so keep an eye on ur mobile or visit www.win-82050.co.uk"
```

Sample output:

```text
label: malicious
confidence: 98.58%
```

The script loads `models/distilbert-sms/`, tokenizes the message, runs the
classifier, and prints the predicted label plus confidence.

## Repository structure

```text
sms-malicious-classifier/
  README.md
  pyproject.toml
  uv.lock
  AGENTS.md
  LEARNINGS.md
  data/
    raw/
    processed/
      train.csv
      validation.csv
      test.csv
  notebooks/
    01_data_exploration.ipynb
    02_train_distilbert.ipynb
    03_evaluate_and_demo.ipynb
  src/
    sms_classifier/
      data.py
      labels.py
      model.py
      predict.py
  scripts/
    predict.py
  models/
    distilbert-sms/
  reports/
    figures/
      confusion_matrix.png
    metrics.json
```

Large generated artifacts, including trained model weights, are ignored by git
by default. If `models/distilbert-sms/` is missing, run the training notebook
before using the CLI.

## Label mapping

The project uses one shared mapping in
[`src/sms_classifier/labels.py`](src/sms_classifier/labels.py):

```python
LABEL_TO_ID = {
    "benign": 0,
    "malicious": 1,
}
```

The same mapping is used for data preparation, training, evaluation, and CLI
prediction.

## Code quality

Ruff is configured as the formatter and linter.

```bash
uv run ruff check .
uv run ruff format --check .
```

## Learning references

- [Jay Alammar — The Illustrated BERT, ELMo, and co.](https://jalammar.github.io/illustrated-bert/)
- [Jay Alammar — The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/)
- [Hugging Face NLP Course — Fine-tuning a pretrained model](https://huggingface.co/learn/nlp-course/chapter3/1)
- [UCI SMS Spam Collection Dataset](https://archive.ics.uci.edu/dataset/228/sms+spam+collection)

## Future work

- Add a true smishing/phishing SMS dataset and compare results against this
  spam/ham proxy baseline.
- Add batch prediction for CSV files.
- Compare DistilBERT with a simple TF-IDF + Logistic Regression baseline.
- Add lightweight tests for data loading, label mapping, and CLI prediction.
- Package a small local demo after the notebook and CLI workflow are stable.
