import numpy as np
import pandas as pd


def add_returns(df):
    df["Return_1D"] = df["Adj Close"].pct_change()

    df["Return_Lag_1"] = df["Return_1D"].shift(1)
    df["Return_Lag_5"] = df["Return_1D"].shift(5)
    df["Return_Lag_10"] = df["Return_1D"].shift(10)
    df["Return_Lag_20"] = df["Return_1D"].shift(20)

    return df


def add_moving_average_features(df):
    sma20 = df["Adj Close"].rolling(20).mean()
    sma50 = df["Adj Close"].rolling(50).mean()
    ema20 = df["Adj Close"].ewm(span=20, adjust=False).mean()

    df["Price_SMA20_Ratio"] = df["Adj Close"] / sma20 - 1
    df["Price_SMA50_Ratio"] = df["Adj Close"] / sma50 - 1
    df["Price_EMA20_Ratio"] = df["Adj Close"] / ema20 - 1

    return df


def add_rsi(df, period=14):
    delta = df["Adj Close"].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(
        alpha=1 / period,
        adjust=False,
        min_periods=period
    ).mean()

    avg_loss = loss.ewm(
        alpha=1 / period,
        adjust=False,
        min_periods=period
    ).mean()

    rs = avg_gain / avg_loss

    df["RSI_14"] = 100 - (100 / (1 + rs))

    return df


def add_macd(df):
    ema12 = df["Adj Close"].ewm(
        span=12,
        adjust=False
    ).mean()

    ema26 = df["Adj Close"].ewm(
        span=26,
        adjust=False
    ).mean()

    df["MACD"] = ema12 - ema26

    df["MACD_Signal"] = df["MACD"].ewm(
        span=9,
        adjust=False
    ).mean()

    return df


def add_bollinger_features(df):
    sma20 = df["Adj Close"].rolling(20).mean()
    std20 = df["Adj Close"].rolling(20).std()

    upper = sma20 + 2 * std20
    lower = sma20 - 2 * std20

    df["BB_%B"] = (df["Adj Close"] - lower) / (upper - lower)

    df["BB_Width"] = (upper - lower) / sma20

    return df


def add_atr(df, period=14):
    previous_close = df["Close"].shift(1)

    tr1 = df["High"] - df["Low"]
    tr2 = (df["High"] - previous_close).abs()
    tr3 = (df["Low"] - previous_close).abs()

    true_range = pd.concat(
        [tr1, tr2, tr3],
        axis=1
    ).max(axis=1)

    atr = true_range.ewm(
        alpha=1 / period,
        adjust=False,
        min_periods=period
    ).mean()

    df["ATR_%"] = atr / df["Close"]

    return df


def add_volatility_features(df):
    df["Volatility_20D"] = (
        df["Return_1D"]
        .rolling(20)
        .std()
    )

    volume_average = df["Volume"].rolling(20).mean()

    df["Relative_Volume"] = (
        df["Volume"] / volume_average
    )

    return df


def create_features(df):
    df = df.copy()

    df = add_returns(df)
    df = add_moving_average_features(df)
    df = add_rsi(df)
    df = add_macd(df)
    df = add_bollinger_features(df)
    df = add_atr(df)
    df = add_volatility_features(df)

    return df