"""Retrain models daily based on trade history."""

from pathlib import Path
import pickle

import pandas as pd
from sklearn.ensemble import RandomForestClassifier


def retrain_model(trade_log_path: str) -> None:
    """Load trade logs and update models per ticker."""
    df = pd.read_csv(trade_log_path)
    model_dir = Path("models")
    model_dir.mkdir(exist_ok=True)

    for ticker in df["Ticker"].unique():
        sub = df[df["Ticker"] == ticker]
        X = sub[["Confidence", "Volume", "Volatility"]]
        y = sub["Success"]

        model = RandomForestClassifier(n_estimators=50)
        model.fit(X, y)

        with open(model_dir / f"{ticker}_model.pkl", "wb") as f:
            pickle.dump(model, f)

        print(f"✅ Retrained model for {ticker}")


if __name__ == "__main__":  # pragma: no cover - example usage
    retrain_model("trade_log.csv")
