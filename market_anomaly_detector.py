import random
import requests
from datetime import datetime


def is_ticker_halted(ticker: str) -> bool:
    """Check if a ticker is halted via placeholder API."""
    url = f"https://finnhub.io/api/v1/stock/halt?symbol={ticker}&token=demo"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200 and r.json():
            return True
    except Exception:
        pass
    return False


def flash_crash_detected(ticker: str) -> bool:
    """Dummy flash crash detector using random chance."""
    return random.random() < 0.005


def check_anomalies(tickers: list[str]) -> list[str]:
    """Return list of tickers with detected anomalies."""
    flagged = []
    for t in tickers:
        if is_ticker_halted(t) or flash_crash_detected(t):
            flagged.append(t)
    if flagged:
        print(f"[{datetime.utcnow()}] \U0001f6a8 Market anomaly detected: {', '.join(flagged)}")
    return flagged


if __name__ == "__main__":
    sample = ["AAPL", "TSLA", "SPY"]
    check_anomalies(sample)
