import time
import pickle
from sklearn.ensemble import RandomForestClassifier
import pandas as pd


def train_and_upload(ticker, data_csv):
    print(f"[CLOUD] 🚀 Uploading {ticker} data...")
    time.sleep(2)

    df = pd.read_csv(data_csv)
    X = df[["Confidence", "Volume", "Volatility"]]
    y = df["Success"]

    model = RandomForestClassifier(n_estimators=100)
    model.fit(X, y)

    with open(f"models/{ticker}_model.pkl", "wb") as f:
        pickle.dump(model, f)
    print(f"[CLOUD] ✅ Model for {ticker} updated via cloud sim.")
