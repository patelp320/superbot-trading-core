import os
import pickle
from datetime import datetime

import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier

LOG_DIR = os.environ.get("LOG_DIR", "logs")
DATA_PATH = os.path.join(LOG_DIR, "trade_journal.csv")
MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)

def train_from_history():
    if not os.path.exists(DATA_PATH):
        print("No trade history found")
        return
    df = pd.read_csv(DATA_PATH)
    required = {"volume", "volatility", "rsi", "macd", "PnL"}
    if not required.issubset(df.columns):
        print("Trade history missing required columns")
        return
    df["label"] = df["PnL"].apply(lambda x: 1 if x > 0 else 0)
    X = df[["volume", "volatility", "rsi", "macd"]]
    y = df["label"]
    model = GradientBoostingClassifier().fit(X, y)
    fname = f"{MODEL_DIR}/self_trained_{datetime.utcnow().date()}.pkl"
    with open(fname, "wb") as f:
        pickle.dump(model, f)
    print(f"Model saved to {fname}")

if __name__ == "__main__":
    train_from_history()
