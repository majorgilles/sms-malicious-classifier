# SMS Malicious Message Classifier

A 2–3 day NLP project that classifies SMS messages as **malicious** or **benign** using a small BERT-style model: **DistilBERT**.

The goal is to build a portfolio-ready `uv` Python project with Jupyter notebooks, a trained model, evaluation results, and a command-line script that can classify one new SMS message.

> **Important limitation:** the first version will use a public SMS spam/ham dataset as a practical proxy for malicious SMS detection. That means it is useful for learning and demonstration, but it is not a complete real-world security detector.

## Project goals

- Use `uv` for Python project and dependency management.
- Use Jupyter notebooks for exploration, training, evaluation, and demo.
- Fine-tune DistilBERT to classify SMS messages as:
  - `malicious`: spam, scam-like, phishing-like, or suspicious messages
  - `benign`: normal messages
- Evaluate with safety-aware metrics:
  - accuracy
  - precision
  - recall
  - F1
  - confusion matrix
- Pay special attention to **malicious-message recall**: how many truly bad messages the model catches.
- Save the trained model and tokenizer.
- Provide a CLI script for one-message prediction.

Example final usage:

```bash
uv run python scripts/predict.py "URGENT: Your account is locked. Click here to verify."
```

Expected final output style:

```text
label: malicious
confidence: 0.94
```

## Plain-English glossary

- **NLP**: Natural Language Processing; teaching computers to work with text.
- **Dataset**: a list of example SMS messages used to train and test the model.
- **Label**: the answer attached to a message, such as `malicious` or `benign`.
- **Spam**: unwanted or junk messages.
- **Ham**: normal, non-spam messages. In this project, ham maps to `benign`.
- **Smishing**: phishing through SMS, often trying to steal money, passwords, or personal information.
- **Proxy**: an imperfect substitute. Here, spam is used as a first approximation of malicious SMS.
- **Model**: the trained program that learns patterns from examples and predicts labels for new messages.
- **DistilBERT**: a smaller, faster version of BERT, a modern language model.
- **Fine-tuning**: taking a pre-trained model and training it a little more on this SMS classification task.
- **GPU**: hardware that can train deep learning models faster than a CPU.
- **CUDA**: NVIDIA software support that lets PyTorch use the GPU.
- **Recall**: of the truly malicious messages, how many the model catches.
- **Precision**: when the model says `malicious`, how often it is correct.
- **F1**: one score that balances precision and recall.
- **Confusion matrix**: a small table showing correct predictions and mistake types.

## Learning references

These are included to guide the learning path while building the project:

1. **Jay Alammar — The Illustrated BERT, ELMo, and co.**  
   A well-known visual blog post explaining BERT-style language models in approachable terms.  
   <https://jalammar.github.io/illustrated-bert/>

2. **Jay Alammar — The Illustrated Transformer**  
   A visual explanation of the transformer architecture behind BERT and DistilBERT.  
   <https://jalammar.github.io/illustrated-transformer/>

3. **Hugging Face NLP Course — Fine-tuning a pretrained model**  
   Practical guide to using transformer models for text classification.  
   <https://huggingface.co/learn/nlp-course/chapter3/1>

4. **UCI SMS Spam Collection Dataset**  
   A classic public SMS spam/ham dataset suitable for a first version of this project.  
   <https://archive.ics.uci.edu/dataset/228/sms+spam+collection>

## Planned repository structure

```text
sms-malicious-classifier/
  README.md
  pyproject.toml
  uv.lock
  .gitignore
  data/
    raw/
    processed/
  notebooks/
    01_data_exploration.ipynb
    02_train_distilbert.ipynb
    03_evaluate_and_demo.ipynb
  src/
    sms_classifier/
      __init__.py
      data.py
      model.py
      predict.py
  scripts/
    predict.py
  models/
    distilbert-sms/
  reports/
    figures/
    metrics.json
  docs/
    github-issues.md
```

## Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd sms-malicious-classifier
```

### 2. Create the environment with uv

```bash
uv sync
```

### 3. Register the Jupyter kernel

```bash
uv run python -m ipykernel install --user --name sms-malicious-classifier --display-name "SMS Malicious Classifier"
```

### 4. Verify GPU support

Because this project targets a local NVIDIA RTX 4070 SUPER, verify that PyTorch can see CUDA:

```bash
uv run python -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU only')"
```

If this prints `False`, the project can still be developed, but DistilBERT training will be slower until CUDA/PyTorch is fixed.

## Code quality

Ruff is configured as the project formatter and linter.

```bash
# Check for lint issues
uv run ruff check .

# Auto-fix lint issues when possible
uv run ruff check --fix .

# Format Python code
uv run ruff format .

# Verify formatting without changing files
uv run ruff format --check .
```

## Notebook plan

### `notebooks/01_data_exploration.ipynb`

Purpose: understand the dataset before modeling.

Main tasks:

- Load the SMS spam/ham dataset.
- Rename labels:
  - `spam` -> `malicious`
  - `ham` -> `benign`
- Check class balance: how many malicious vs benign messages exist.
- Inspect example messages.
- Split data into train/validation/test sets.
- Save processed data under `data/processed/`.

### `notebooks/02_train_distilbert.ipynb`

Purpose: fine-tune DistilBERT.

Main tasks:

- Load processed SMS data.
- Load DistilBERT tokenizer and model from Hugging Face.
- Tokenize SMS messages.
- Train/fine-tune the model.
- Save the trained model and tokenizer to `models/distilbert-sms/`.

### `notebooks/03_evaluate_and_demo.ipynb`

Purpose: evaluate and demonstrate the trained model.

Main tasks:

- Load the saved model.
- Evaluate on the test set.
- Report accuracy, precision, recall, F1, and confusion matrix.
- Save metrics to `reports/metrics.json`.
- Show example predictions.
- Explain limitations and next steps.

## CLI prediction plan

The final script should classify one message at a time:

```bash
uv run python scripts/predict.py "Free prize! Claim now at this link"
```

Possible output:

```text
label: malicious
confidence: 0.91
```

Example commands:

```bash
uv run python scripts/predict.py "Hey, are we still meeting at 6?"
uv run python scripts/predict.py "URGENT: Your account is locked. Click here to verify."
uv run python scripts/predict.py "Congratulations! You won a free prize. Claim now."
```

The script should:

1. Load `models/distilbert-sms/`.
2. Tokenize the input SMS.
3. Run the model.
4. Convert model output into a label and confidence score.
5. Print the result clearly.

## 2–3 day build plan

### Day 1: Project setup and data

- Finalize `uv` project setup.
- Add notebook dependencies.
- Download/load the SMS dataset.
- Explore examples and class balance.
- Create train/validation/test splits.
- Write clear notes explaining dataset limitations.

### Day 2: Train DistilBERT

- Verify local GPU/CUDA support.
- Fine-tune DistilBERT.
- Save the model and tokenizer.
- Track basic training results.

### Day 3: Evaluate, demo, and polish

- Evaluate using safety-aware metrics.
- Create confusion matrix visualization.
- Implement `scripts/predict.py`.
- Add example predictions.
- Polish README and notebooks for portfolio use.

## Risks and scope control

- DistilBERT setup can be fragile because PyTorch, CUDA, and Hugging Face dependencies must work together.
- The dataset is a first-version proxy, not a complete malicious-SMS security dataset.
- Do not add deployment or a web app until the notebooks, saved model, metrics, and CLI work.
- If training becomes slow, reduce epochs, batch size, or max sequence length before expanding scope.

## Future improvements

- Add a true smishing/phishing SMS dataset.
- Compare DistilBERT against a simple TF-IDF + Logistic Regression baseline.
- Add batch CSV prediction.
- Add tests for data loading and CLI prediction.
- Package the model for a small local web demo.
