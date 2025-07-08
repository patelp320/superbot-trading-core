import random
import json
import sys
from datetime import datetime

TICKERS = sys.argv[1:] or ["AAPL"]


def predict_volatility(ticker: str) -> float:
    """Return dummy predicted volatility."""
    return random.uniform(0.01, 0.1)


def main():
    preds = {t: predict_volatility(t) for t in TICKERS}
    path = "../data/volatility.json"
    with open(path, "w") as f:
        json.dump(preds, f)
    print(f"[{datetime.utcnow()}] ⚡ Volatility predictions saved -> {path}")


def load_predictions() -> dict:
    try:
        with open("../data/volatility.json", "r") as f:
            return json.load(f)
    except Exception:
        return {}


if __name__ == "__main__":
    main()
