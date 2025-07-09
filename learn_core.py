import logging; logging.basicConfig(level=logging.INFO)
import yfinance as yf
import pandas as pd
from datetime import datetime, timezone
import pickle
import os
import requests
from io import StringIO
import time
import config
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
import random

# Additional macro symbols for feature engineering
MACRO_SYMBOLS = {
    "SPY": "SPY",
    "VIX": "^VIX",
    "TNX": "^TNX",
    "OIL": "CL=F",
}

MODEL_DIR = "../models"
os.makedirs(MODEL_DIR, exist_ok=True)

# Limit the number of tickers scanned to avoid extremely long runtimes.
# Uses the value configured in config.py
MAX_TICKERS = config.MAX_SCAN_TICKERS

def fetch_macro_features():
    """Return latest macro indicators used as features."""
    features = {}
    for name, symbol in MACRO_SYMBOLS.items():
        try:
            df = yf.download(symbol, period="5d", interval="1d", progress=False)
            features[name] = float(df["Close"].iloc[-1].item()) if not df.empty else 0.0
        except Exception:
            features[name] = 0.0
    return features

MACRO_FEATURES = fetch_macro_features()


def fallback_tickers():
    """Return a static list of tickers if NASDAQ fetch fails."""
    print("📄 Using local backup ticker list...")
    return [
        "GFAI",
        "SNTI",
        "COSM",
        "HILS",
        "NVOS",
        "TOP",
        "CVNA",
        "TSLA",
        "AAPL",
        "QQQ",
    ]


def fetch_from_nasdaq():
    """Fetch the current NASDAQ listed tickers."""
    print(f"[{datetime.now(timezone.utc)}] \U0001f310 Fetching tickers from NASDAQ Trader...")
    url = "https://www.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt"
    df = pd.read_csv(StringIO(requests.get(url, timeout=10).text), sep="|")
    tickers = df["Symbol"].dropna().tolist()
    return tickers[:-1]

def manage_models():
    models = []
    for file in os.listdir(MODEL_DIR):
        if file.endswith(".pkl"):
            with open(os.path.join(MODEL_DIR, file), "rb") as f:
                m = pickle.load(f)
                score = m["avg_return"] / m["volatility"] if m["volatility"] else 0
                models.append((score, file))
    models.sort(reverse=True)
    for _, file in models[5:]:
        os.remove(os.path.join(MODEL_DIR, file))

def fetch_all_tickers():
    """Get tickers from NASDAQ with a local fallback."""
    try:
        tickers = fetch_from_nasdaq()
    except Exception as e:
        print(f"❌ Ticker fetch failed: {e}")
        tickers = fallback_tickers()
    return tickers

def process_ticker_data(ticker, df):
    """Generate and persist model data using a pre-fetched dataframe."""
    if df.empty:
        return None

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(-1)
    if "Close" not in df.columns or not pd.api.types.is_numeric_dtype(df["Close"]):
        return None

    df = df.dropna(subset=["Close", "Volume"])
    if df.empty:
        return None

    latest_price = df["Close"].iloc[-1]
    avg_volume = df["Volume"].tail(5).mean()
    todays_volume = df["Volume"].iloc[-1]
    vwap = (df["Close"] * df["Volume"]).sum() / df["Volume"].sum()
    vwap_dist = latest_price - vwap
    rel_volume = todays_volume / df["Volume"].mean()
    gap_pct = 0.0
    if len(df) > 1 and "Open" in df.columns:
        prev_close = df["Close"].iloc[-2]
        open_today = df["Open"].iloc[-1]
        if prev_close:
            gap_pct = (open_today - prev_close) / prev_close

    # Skip tiny liquidity
    if avg_volume < 50000:
        return None

    is_penny = latest_price < 5.00

    df["Return"] = df["Close"].pct_change()
    avg_return = df["Return"].mean()
    volatility = df["Return"].std()

    macro = MACRO_FEATURES

    model = {
        "ticker": ticker,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "avg_return": avg_return,
        "volatility": volatility,
        "is_penny": is_penny,
        "price": latest_price,
        "avg_volume": avg_volume,
        "vwap_dist": vwap_dist,
        "rel_volume": rel_volume,
        "gap_pct": gap_pct,
        "macro": macro,
    }

    with open(f"{MODEL_DIR}/{ticker}_{datetime.now(timezone.utc).date()}.pkl", "wb") as f:
        pickle.dump(model, f)

    tag = "🪙 PENNY" if is_penny else "💼"
    print(f"[{datetime.now(timezone.utc)}] ✅ {ticker} model saved. {tag}")
    return ticker


def process_ticker(ticker):
    """Fetch data for a single ticker then process it."""
    try:
        df = yf.download(
            ticker,
            period="30d",
            interval="1d",
            progress=False,
            auto_adjust=True,
        )
        return process_ticker_data(ticker, df)
    except Exception as e:
        print(f"[{datetime.now(timezone.utc)}] ❌ {ticker} failed: {e}")
        return None

def walk_forward_optimization(model):
    # Placeholder for future walk-forward optimization logic
    pass

def reinforcement_learning_module(data):
    # Placeholder for Q-learning based entry/exit logic
    pass


def analyze_penny_trades(log_path="../logs/penny_trade_log.csv"):
    if not os.path.exists(log_path):
        return {}
    df = pd.read_csv(log_path, names=["Ticker", "Entry", "Exit", "Strategy", "Pct"], header=None)
    df.dropna(inplace=True)
    summary = df.groupby("Ticker")["Pct"].agg(["count", "mean"]).reset_index()
    summary.rename(columns={"count": "trades", "mean": "avg_pct"}, inplace=True)
    best = summary.sort_values("avg_pct", ascending=False).head(3)
    best_str = "; ".join(f"{row.Ticker}:{round(row.avg_pct,2)}%" for _, row in best.iterrows())
    with open("../logs/learn.log", "a") as f:
        f.write(f"[{datetime.now(timezone.utc)}] 📊 Penny trade analysis: {best_str}\n")
    return summary

# --- Fast multithreaded scanning utilities ---
def scan_batch(tickers):
    """Download a batch of tickers and process those trading under $5."""
    try:
        df = yf.download(
            tickers=tickers,
            period="30d",
            interval="1d",
            group_by="ticker",
            auto_adjust=True,
            progress=False,
            threads=True,
        )
        results = {}
        for ticker in tickers:
            try:
                data = df[ticker] if isinstance(df.columns, pd.MultiIndex) else df
                if not data.empty:
                    last_close = float(data["Close"].iloc[-1])
                    if last_close < 5:
                        results[ticker] = last_close
                        process_ticker_data(ticker, data)
            except Exception:
                continue
        return results
    except Exception as e:
        print(f"\u274c Batch failed: {e}")
        return {}


def chunk(lst, size):
    """Yield successive chunks from list."""
    for i in range(0, len(lst), size):
        yield lst[i : i + size]

if __name__ == "__main__":
    tickers = fetch_all_tickers()
    tickers = [t for t in tickers if t.isalpha()]
    if len(tickers) > MAX_TICKERS:
        tickers = random.sample(tickers, MAX_TICKERS)
    print(
        f"[{datetime.now(timezone.utc)}] 🚀 Starting fast scan of {len(tickers)} tickers using thread pool..."
    )

    batches = list(chunk(tickers, 100))
    total_found = 0
    features = {}

    max_threads = min(8, os.cpu_count() or 4)
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        future_to_batch = {executor.submit(scan_batch, batch): batch for batch in batches}
        for i, future in enumerate(as_completed(future_to_batch)):
            batch_result = future.result()
            for ticker, price in batch_result.items():
                features[ticker] = price
            total_found += len(batch_result)
            print(
                f"✅ Completed batch {i+1}/{len(batches)} — total tickers found: {total_found}"
            )

    print("✅ Scan complete.")

    # Write scan results for debugging
    with open("scan_results.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["Ticker", "Last Close"])
        for t, p in features.items():
            writer.writerow([t, p])

    # Export penny stock watchlist for other modules
    os.makedirs("../logs", exist_ok=True)
    watchlist_path = "../logs/penny_watchlist.txt"
    with open(watchlist_path, "w") as f:
        for ticker, price in sorted(features.items(), key=lambda x: x[1]):
            f.write(f"{ticker}\n")

    manage_models()
    analyze_penny_trades()
