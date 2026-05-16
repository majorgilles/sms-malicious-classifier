# AGENTS.md

## Project overview

This project is a Python NLP portfolio project for classifying SMS messages as
`malicious` or `benign` using a fine-tuned DistilBERT model.

The project uses:

- `uv` for dependency and environment management
- Hugging Face `transformers` and `datasets`
- PyTorch for model training
- Jupyter notebooks for exploration, training, and evaluation
- Ruff for formatting and linting

## Project structure

Expected repository layout:

```text
sms-malicious-classifier/
  README.md
  pyproject.toml
  AGENTS.md
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
      __init__.py
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
    metrics.json
```

Keep reusable Python logic in `src/sms_classifier/`.

Use notebooks for explanation, experimentation, and portfolio narrative, but avoid
burying important reusable logic only inside notebooks.

## Python style

Follow the Ruff configuration in `pyproject.toml`.

Project conventions:

- Use Python 3.11+ syntax.
- Use double quotes for strings.
- Keep lines at or below 88 characters where practical.
- Keep imports sorted.
- Prefer small, focused functions.
- Prefer clear names over abbreviations.
- Avoid unnecessary comments that repeat the code.
- Add comments only when they explain non-obvious reasoning.

Run these checks before considering work complete:

```bash
uv run ruff check .
uv run ruff format --check .
```

## Typing conventions

Use type hints for reusable project code, especially code under
`src/sms_classifier/`.

Expected typing style:

- Add return types to functions.
- Type important constants when helpful.
- Use built-in generic types such as `dict[str, int]` and `list[str]`.
- Use `str | Path` for functions that accept filesystem paths.
- Use concrete domain types where useful, for example:
  - `pd.DataFrame` for pandas dataframes
  - `PreTrainedTokenizerBase` for Hugging Face tokenizers
  - `PreTrainedModel` for Hugging Face models
- Avoid `Any` unless there is a clear reason.
- Do not add complicated typing just for its own sake.

Example:

```python
from pathlib import Path

import pandas as pd


def save_splits(
    train_df: pd.DataFrame,
    validation_df: pd.DataFrame,
    test_df: pd.DataFrame,
    output_dir: str | Path = "data/processed",
) -> None:
    ...
```

## Label conventions

Use these project labels consistently:

- `benign`
- `malicious`

Use shared label mappings instead of redefining them in multiple places.

Preferred location:

```text
src/sms_classifier/labels.py
```

Expected mappings:

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

The same mapping must be used for training, evaluation, and prediction.

## Model conventions

The first model target is:

```text
distilbert-base-uncased
```

Reusable model helpers should live in:

```text
src/sms_classifier/model.py
```

Training should save the model and tokenizer to:

```text
models/distilbert-sms/
```

Keep training configuration small enough for the project scope. Prefer fast,
understandable experiments over large hyperparameter searches.

## Notebook conventions

Notebooks should be readable as a portfolio walkthrough.

Each notebook should include:

- A short purpose statement
- Clear section headings
- Plain-English explanations
- Code cells that call reusable helpers where appropriate
- Outputs or saved artifacts that support the GitHub issue acceptance criteria

Notebook roles:

- `01_data_exploration.ipynb`: load data, map labels, inspect class balance,
  save splits
- `02_train_distilbert.ipynb`: tokenize data, fine-tune DistilBERT, save model
- `03_evaluate_and_demo.ipynb`: evaluate metrics, save reports, show examples

## Data and artifact conventions

Generated or downloaded data should stay under:

```text
data/
```

Trained models should stay under:

```text
models/
```

Evaluation outputs should stay under:

```text
reports/
```

Do not commit large generated artifacts unless the project explicitly decides to
track them.

## Scope control

This is a 2-3 day learning project.

Prefer:

- simple reusable helpers
- clear notebooks
- working end-to-end training
- readable evaluation results

Avoid adding unrelated features such as:

- web apps
- deployment infrastructure
- batch prediction
- large model comparisons

Those belong in future improvements after the core workflow works.
