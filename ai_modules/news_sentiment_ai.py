"""TODO: Add module description for news_sentiment_ai."""

import random
import json
import sys
from datetime import datetime, timezone

TICKERS = sys.argv[1:] or ["AAPL", "TSLA", "SPY"]


def score_ticker(ticker: str) -> float:
    """Placeholder for real news + social sentiment scoring."""
    return random.uniform(-1, 1)


def main():
    scores = {t: score_ticker(t) for t in TICKERS}
    path = "../data/news_sentiment.json"
    with open(path, "w") as f:
        json.dump(scores, f)
    print(f"[{datetime.now(timezone.utc)}] 📰 Sentiment scores saved -> {path}")


def load_scores() -> dict:
    try:
        with open("../data/news_sentiment.json", "r") as f:
            return json.load(f)
    except Exception:
        return {}


if __name__ == "__main__":
    main()
