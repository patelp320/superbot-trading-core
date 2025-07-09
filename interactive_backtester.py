"""Quick backtesting utility via Streamlit."""
import importlib

import pandas as pd
import yfinance as yf


def run_backtest(ticker: str, strategy_name: str, start: str, end: str):
    """Backtest a strategy on a ticker and return simple metrics."""
    strat = importlib.import_module(f"strategies.{strategy_name}")
    df = yf.download(ticker, start=start, end=end, progress=False)
    df["Signal"] = df["Close"].rolling(5).mean() > df["Close"]

    trades = []
    for i in range(5, len(df)):
        if hasattr(strat, "run") and strat.run(df.iloc[:i]) == "BUY":
            trades.append(df["Close"].iloc[i])

    win_rate = (
        sum(1 for t in trades if t < df["Close"].iloc[-1]) / len(trades)
        if trades
        else 0
    )
    pnl = sum(df["Close"].iloc[-1] - t for t in trades)
    drawdown = (
        min(
            df["Close"].iloc[i] - min(df["Close"].iloc[i : i + 5])
            for i in range(len(df) - 5)
        )
        if len(df) >= 5
        else 0
    )

    return {"wins": win_rate, "pnl": pnl, "drawdown": drawdown}


if __name__ == "__main__":  # pragma: no cover - simple usage example
    print(run_backtest("SPY", "alpha_dummy", "2020-01-01", "2020-06-01"))
