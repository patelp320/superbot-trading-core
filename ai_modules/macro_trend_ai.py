import random
from datetime import datetime, timezone
import os

import pandas as pd
import yfinance as yf

REGIMES = ["BULL", "BEAR", "CHOPPY"]


def detect_regime() -> str:
    """Classify market regime using SPY moving averages.

    Falls back to a random choice on failure so the rest of the
    system can continue operating during data issues.
    """
    try:
        spy = yf.download("SPY", period="1y", progress=False)
        if spy.empty:
            raise ValueError("No data returned")
        sma50 = spy["Close"].rolling(50).mean().iloc[-1]
        sma200 = spy["Close"].rolling(200).mean().iloc[-1]
        if sma50 > sma200:
            return "BULL"
        elif sma50 < sma200:
            return "BEAR"
        else:
            return "CHOPPY"
    except Exception:
        return random.choice(REGIMES)


def main():
    regime = detect_regime()
    os.makedirs("../data", exist_ok=True)
    with open("../data/macro_regime.txt", "w") as f:
        f.write(regime)
    print(f"[{datetime.now(timezone.utc)}] 🌎 Market regime -> {regime}")


def current_regime() -> str:
    try:
        with open("../data/macro_regime.txt", "r") as f:
            regime = f.read().strip()
            if regime:
                return regime
    except Exception:
        pass
    return detect_regime()


if __name__ == "__main__":
    main()
