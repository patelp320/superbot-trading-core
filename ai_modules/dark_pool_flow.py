import random
from datetime import datetime, timezone


def fetch_dark_pool_volume(ticker: str) -> float:
    """Return dummy dark pool volume."""
    return random.uniform(0, 1_000_000)


def fetch_open_interest(ticker: str) -> float:
    """Return dummy open interest."""
    return random.uniform(0, 100_000)


def fetch_put_call_ratio(ticker: str) -> float:
    """Return dummy put/call ratio."""
    return random.uniform(0.5, 2.0)


def flag_unusual_activity(tickers: list[str]) -> list[str]:
    flagged = []
    for t in tickers:
        dark_vol = fetch_dark_pool_volume(t)
        oi = fetch_open_interest(t)
        pcr = fetch_put_call_ratio(t)
        if dark_vol > 500_000 or oi > 50_000 or pcr > 1.5:
            flagged.append(t)
    if flagged:
        print(f"[{datetime.now(timezone.utc)}] \U0001f50e Unusual flow: {', '.join(flagged)}")
    return flagged


if __name__ == "__main__":
    sample = ["AAPL", "TSLA", "SPY"]
    flag_unusual_activity(sample)
