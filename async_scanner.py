"""Async ticker scanning utility."""

import asyncio
from datetime import datetime
from typing import Dict, List, Tuple

import pandas as pd
import yfinance as yf


def _fetch_sync(ticker: str) -> pd.DataFrame:
    """Synchronous wrapper around ``yf.download`` for a single ticker."""
    return yf.download(ticker, period="1d", interval="1m", progress=False)


async def fetch_ticker(ticker: str) -> Tuple[str, pd.DataFrame]:
    """Fetch price data for ``ticker`` asynchronously."""
    loop = asyncio.get_running_loop()
    df = await loop.run_in_executor(None, _fetch_sync, ticker)
    ts = datetime.utcnow().strftime("%H:%M:%S")
    print(f"[{ts}] ✅ {ticker} fetched")
    return ticker, df


async def scan_tickers(tickers: List[str]) -> Dict[str, pd.DataFrame]:
    """Download data for a list of ``tickers`` concurrently."""
    results = await asyncio.gather(*(fetch_ticker(t) for t in tickers))
    return dict(results)


if __name__ == "__main__":  # pragma: no cover - example usage
    sample = ["TSLA", "AAPL", "MSFT"]
    data = asyncio.run(scan_tickers(sample))
    print({t: df.head() for t, df in data.items()})
