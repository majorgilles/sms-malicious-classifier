"""Predict whether one SMS message is malicious or benign.

This is a placeholder for the final CLI. Issue #5 will replace this with code
that loads the saved DistilBERT model from models/distilbert-sms/.
"""

from __future__ import annotations

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="Classify one SMS message.")
    parser.add_argument("message", help="SMS message text to classify")
    args = parser.parse_args()

    raise SystemExit(
        "Prediction is not implemented yet. "
        "Train and save the DistilBERT model first, then update scripts/predict.py.\n"
        f"Received message: {args.message!r}"
    )


if __name__ == "__main__":
    main()
