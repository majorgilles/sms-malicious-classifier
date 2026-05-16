from sms_classifier.data import load_sms_dataset, split_sms_dataset

if __name__ == "__main__":
    df = load_sms_dataset()
    train_df, validation_df, test_df = split_sms_dataset(df)

    print(train_df.shape)
    print(validation_df.shape)
    print(test_df.shape)

    print(train_df["label"].value_counts(normalize=True))
    print(validation_df["label"].value_counts(normalize=True))
    print(test_df["label"].value_counts(normalize=True))
