"""Fetch ticker data with automatic fallback on failure."""

import os

import pandas as pd
import yfinance as yf


def fetch_data(ticker: str):
    """Return recent data for ``ticker`` with failover to CSV."""
    try:
        df = yf.download(ticker, "5d", "1m", progress=False)
        if df.empty:
            raise ValueError("Empty from yfinance")
        print(f"✅ {ticker} loaded from yfinance")
        return df
    except Exception as exc:
        print(f"⚠️ yfinance failed: {exc}")
        alt_path = f"backup_data/{ticker}.csv"
        if os.path.exists(alt_path):
            df = pd.read_csv(alt_path)
            print(f"📂 {ticker} loaded from fallback CSV")
            return df
        print(f"❌ No data available for {ticker}")
        return None


if __name__ == "__main__":  # pragma: no cover - example usage
    fetch_data("AAPL")
