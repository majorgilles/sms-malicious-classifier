from pathlib import Path

import pandas as pd
from datasets import load_dataset
from sklearn.model_selection import train_test_split

DATASET_NAME = "ucirvine/sms_spam"
LABEL_MAP = {0: "benign", 1: "malicious"}


def load_sms_dataset() -> pd.DataFrame:
    dataset = load_dataset(DATASET_NAME, split="train")

    df = dataset.to_pandas()
    df = df.rename(columns={"sms": "message"})
    df["label"] = df["label"].map(
        LABEL_MAP
    )  # Takes numeric labels and replaces them using LABEL_MAP

    return df[["message", "label"]]  # Returns only those two columns, in that order


def split_sms_dataset(
    df: pd.DataFrame,
    test_size: float = 0.2,
    validation_size: float = 0.1,
    random_state: int = 42,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    train_df, test_df = train_test_split(
        df,
        test_size=test_size,
        random_state=random_state,
        stratify=df["label"],
    )

    """This is the trickiest line.
    We want final sizes:

    - test = 20% of full data
    - validation = 10% of full data
    - train = 70% of full data
    
    But after removing test, only 80% of the original data remains. 
    
    So validation must be:
    ```python
    0.1 / 0.8 = 0.125
    ```
    This is the correct proportion to get 12.5% of the overall remaining train_df., 
    which is 10% over the beginning pool we started up with.
    """
    relative_validation_size = validation_size / (1 - test_size)

    train_df, validation_df = train_test_split(
        train_df,
        test_size=relative_validation_size,
        random_state=random_state,
        stratify=train_df["label"],
    )
    # Without reset_index, the split DataFrames keep their original row numbers,
    # like 104, 982, 7, etc. # With reset, each split starts at 0, 1, 2....
    return (
        train_df.reset_index(drop=True),
        validation_df.reset_index(drop=True),
        test_df.reset_index(drop=True),
    )


def save_splits(
    train_df: pd.DataFrame,
    validation_df: pd.DataFrame,
    test_df: pd.DataFrame,
    output_dir: str | Path = "data/processed",
) -> None:
    output_path = Path(output_dir)
    # exist_ok=True: don’t crash if data/processed/ already exists
    output_path.mkdir(parents=True, exist_ok=True)

    # index=False means: don’t save pandas’ row numbers as an extra CSV column
    train_df.to_csv(output_path / "train.csv", index=False)
    validation_df.to_csv(output_path / "validation.csv", index=False)
    test_df.to_csv(output_path / "test.csv", index=False)
