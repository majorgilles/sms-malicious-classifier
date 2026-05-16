# GitHub issues

These issues are designed as small vertical slices. Each issue should produce something demoable or verifiable, not just a hidden code change.

> Status: created on GitHub for <https://github.com/majorgilles/sms-malicious-classifier>.

## Created issue links

- [#1 Complete reproducible uv + Jupyter project setup](https://github.com/majorgilles/sms-malicious-classifier/issues/1)
- [#2 Build the data exploration notebook and label mapping](https://github.com/majorgilles/sms-malicious-classifier/issues/2)
- [#3 Fine-tune DistilBERT on the SMS dataset](https://github.com/majorgilles/sms-malicious-classifier/issues/3)
- [#4 Evaluate the model with safety-aware metrics](https://github.com/majorgilles/sms-malicious-classifier/issues/4)
- [#5 Implement the one-message prediction CLI](https://github.com/majorgilles/sms-malicious-classifier/issues/5)
- [#6 Polish the portfolio README and final demo narrative](https://github.com/majorgilles/sms-malicious-classifier/issues/6)

## Issue 1: Complete reproducible uv + Jupyter project setup

**Labels:** `type:implementation`, `area:project-setup`, `priority:high`

### What to build

Set up the project so a fresh clone can install dependencies, open notebooks, and verify whether PyTorch can use the local NVIDIA GPU.

### Acceptance criteria

- [ ] `pyproject.toml` includes the main dependencies for notebooks, data work, Hugging Face Transformers, PyTorch, evaluation, and plotting.
- [ ] `uv sync` creates a working local environment.
- [ ] A Jupyter kernel can be registered and selected from notebooks.
- [ ] A documented GPU check command prints whether CUDA is available and, if available, the GPU name.
- [ ] The repository has the expected folders: `data/`, `notebooks/`, `src/`, `scripts/`, `models/`, and `reports/`.

### Blocked by

None - can start immediately.

---

## Issue 2: Build the data exploration notebook and label mapping

**Labels:** `type:implementation`, `area:data`, `area:notebook`, `priority:high`

### What to build

Create `notebooks/01_data_exploration.ipynb` and supporting data code that loads a public SMS spam/ham dataset, maps the labels into the project language, and saves clean train/validation/test splits.

### Acceptance criteria

- [ ] The notebook loads the SMS dataset from a reproducible public source.
- [ ] Labels are mapped clearly: `spam` -> `malicious`, `ham` -> `benign`.
- [ ] The notebook shows class counts and several example messages from each class.
- [ ] The notebook explains that spam is being used as a first-version proxy for malicious SMS.
- [ ] Processed train/validation/test files are saved under `data/processed/`.
- [ ] Reusable loading/splitting logic lives in `src/sms_classifier/data.py`.

### Blocked by

- Issue 1: Complete reproducible uv + Jupyter project setup

---

## Issue 3: Fine-tune DistilBERT on the SMS dataset

**Labels:** `type:implementation`, `area:model`, `area:notebook`, `priority:high`

### What to build

Create `notebooks/02_train_distilbert.ipynb` and supporting model code that fine-tunes DistilBERT for binary malicious-vs-benign SMS classification.

### Acceptance criteria

- [ ] The notebook loads the processed train/validation/test splits.
- [ ] The notebook loads a DistilBERT tokenizer and sequence classification model.
- [ ] SMS messages are tokenized with a clear maximum length suitable for short texts.
- [ ] Training uses the local GPU when CUDA is available.
- [ ] Training configuration is small enough for the 2–3 day project scope.
- [ ] The trained model and tokenizer are saved to `models/distilbert-sms/`.
- [ ] Reusable model/prediction helpers live in `src/sms_classifier/model.py` or similar.

### Blocked by

- Issue 2: Build the data exploration notebook and label mapping

---

## Issue 4: Evaluate the model with safety-aware metrics

**Labels:** `type:implementation`, `area:evaluation`, `area:notebook`, `priority:high`

### What to build

Create `notebooks/03_evaluate_and_demo.ipynb` sections that load the saved model, evaluate it on the held-out test set, and explain the results in plain language.

### Acceptance criteria

- [ ] Evaluation reports accuracy, precision, recall, and F1.
- [ ] Evaluation includes a confusion matrix.
- [ ] The notebook highlights malicious-message recall and explains why missed bad messages matter.
- [ ] Metrics are saved to `reports/metrics.json`.
- [ ] Confusion matrix or other useful plots are saved under `reports/figures/`.
- [ ] The notebook includes a short limitations section explaining that the dataset is a proxy.

### Blocked by

- Issue 3: Fine-tune DistilBERT on the SMS dataset

---

## Issue 5: Implement the one-message prediction CLI

**Labels:** `type:implementation`, `area:cli`, `area:model`, `priority:high`

### What to build

Replace the placeholder `scripts/predict.py` with a command-line script that loads the saved DistilBERT model and classifies one SMS message.

### Acceptance criteria

- [ ] Running `uv run python scripts/predict.py "message text"` loads the saved model from `models/distilbert-sms/`.
- [ ] The script prints a clear label: `malicious` or `benign`.
- [ ] The script prints a confidence score.
- [ ] The script handles empty input with a helpful error message.
- [ ] At least three example commands are documented in the README.
- [ ] Prediction logic is reusable from `src/sms_classifier/predict.py`.

### Blocked by

- Issue 3: Fine-tune DistilBERT on the SMS dataset

---

## Issue 6: Polish the portfolio README and final demo narrative

**Labels:** `type:documentation`, `area:readme`, `priority:medium`

### What to build

Update the README after the model and CLI work so the repository tells a clear portfolio story: what was built, how to run it, what the results mean, and what the limitations are.

### Acceptance criteria

- [ ] README includes final setup commands using `uv`.
- [ ] README includes the final notebook workflow.
- [ ] README includes final CLI examples and sample output.
- [ ] README summarizes evaluation results from `reports/metrics.json`.
- [ ] README links to learning resources, including Jay Alammar's BERT/Transformer explanations and the Hugging Face NLP course.
- [ ] README explains the dataset limitation in plain language.
- [ ] README includes a short future-work section for smishing/phishing data and batch prediction.

### Blocked by

- Issue 4: Evaluate the model with safety-aware metrics
- Issue 5: Implement the one-message prediction CLI
