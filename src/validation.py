def validate_stock_data(df):

    required_columns = [
        "Date",
        "Open",
        "High",
        "Low",
        "Close",
        "Adj Close",
        "Volume"
    ]

    missing_columns = []
    for col in required_columns:
        if col not in df.columns:
            missing_columns.append(col)

    if missing_columns:
        raise ValueError(f"Missing columns: {missing_columns}")

    if df["Date"].duplicated().any():
        raise ValueError("Duplicate dates found")

    if not df["Date"].is_monotonic_increasing:
        raise ValueError("Dates are not sorted")

    if df[required_columns].isnull().any().any():
        raise ValueError("Missing values found")

    if (df["High"] < df["Low"]).any():
        raise ValueError("High price is lower than Low price")

    if (df["High"] < df["Open"]).any():
        raise ValueError("High price is lower than Open price")

    if (df["High"] < df["Close"]).any():
        raise ValueError("High price is lower than Close price")

    if (df["Low"] > df["Open"]).any():
        raise ValueError("Low price is higher than Open price")

    if (df["Low"] > df["Close"]).any():
        raise ValueError("Low price is higher than Close price")

    if (df["Volume"] < 0).any():
        raise ValueError("Negative volume found")

    return True