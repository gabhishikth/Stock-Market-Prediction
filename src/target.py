def create_target(df):
    df = df.copy()

    future_close = df["Close"].shift(-1)

    df["Target"] = (
        future_close > df["Close"]
    ).astype("float")

    df.loc[future_close.isna(), "Target"] = float("nan")

    return df