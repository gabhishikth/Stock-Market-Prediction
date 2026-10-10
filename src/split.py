
import pandas as pd


def chronological_split(
    df,
    train_ratio=0.70,
    val_ratio=0.15
):
    if not 0 < train_ratio < 1:
        raise ValueError("train_ratio must be between 0 and 1")

    if not 0 < val_ratio < 1:
        raise ValueError("val_ratio must be between 0 and 1")

    if train_ratio + val_ratio >= 1:
        raise ValueError("train_ratio + val_ratio must be less than 1")

    if not df["Date"].is_monotonic_increasing:
        raise ValueError("Data must be sorted by Date")

    if df["Date"].duplicated().any():
        raise ValueError("Duplicate dates found")

    n = len(df)

    train_end = int(n * train_ratio)
    val_end = int(n * (train_ratio + val_ratio))

    train_df = df.iloc[:train_end].copy()
    val_df = df.iloc[train_end:val_end].copy()
    test_df = df.iloc[val_end:].copy()

    return train_df, val_df, test_df
