"""TODO: Add module description for flow_analysis_ai."""

import random
import json
import sys
from datetime import datetime, timezone

TICKERS = sys.argv[1:] or ["AAPL", "TSLA"]


def analyze_flow(ticker: str) -> float:
    """Placeholder for unusual options flow scoring."""
    return random.uniform(-1, 1)


def main():
    scores = {t: analyze_flow(t) for t in TICKERS}
    path = "../data/flow_scores.json"
    with open(path, "w") as f:
        json.dump(scores, f)
    print(f"[{datetime.now(timezone.utc)}] 💰 Flow scores saved -> {path}")


def load_flow_scores() -> dict:
    try:
        with open("../data/flow_scores.json", "r") as f:
            return json.load(f)
    except Exception:
        return {}


if __name__ == "__main__":
    main()
