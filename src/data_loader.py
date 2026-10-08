import pandas as pd

def load_stock_data(filepath):
    df = pd.read_csv(filepath)
    
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").reset_index(drop = True)
    return df