"""Classify one SMS message from the command line."""

from __future__ import annotations

import argparse

from sms_classifier.predict import predict_message


def main() -> None:
    parser = argparse.ArgumentParser(description="Classify one SMS message.")
    parser.add_argument("message", help="SMS message text to classify")
    args = parser.parse_args()

    try:
        label, confidence = predict_message(args.message)
    except ValueError as error:
        raise SystemExit(f"Error: {error}") from error

    print(f"label: {label}")
    print(f"confidence: {confidence:.2%}")


if __name__ == "__main__":
    main()
