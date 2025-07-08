import yfinance as yf
import pandas as pd
from datetime import datetime
import pickle
import os
import requests
import concurrent.futures
from io import StringIO
import time

# Additional macro symbols for feature engineering
MACRO_SYMBOLS = {
    "SPY": "SPY",
    "VIX": "^VIX",
    "TNX": "^TNX",
    "OIL": "CL=F",
}

MODEL_DIR = "../models"
os.makedirs(MODEL_DIR, exist_ok=True)

def fetch_macro_features():
    """Return latest macro indicators used as features."""
    features = {}
    for name, symbol in MACRO_SYMBOLS.items():
        try:
            df = yf.download(symbol, period="5d", interval="1d", progress=False)
            features[name] = float(df["Close"].iloc[-1]) if not df.empty else 0.0
        except Exception:
            features[name] = 0.0
    return features

MACRO_FEATURES = fetch_macro_features()

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
    try:
        print(f"[{datetime.utcnow()}] 🌐 Fetching tickers from NASDAQ Trader...")
        url = "https://www.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt"
        df = pd.read_csv(StringIO(requests.get(url, timeout=10).text), sep="|")
        tickers = df["Symbol"].dropna().tolist()
        return tickers[:-1]
    except Exception as e:
        print(f"[{datetime.utcnow()}] ❌ Ticker fetch failed: {e}")
        return ["AAPL", "TSLA", "NVDA", "SPY", "MSFT"]

def process_ticker(ticker):
    try:
        df = yf.download(
            ticker,
            period="30d",
            interval="1d",
            progress=False,
            auto_adjust=True,
        )
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
            "timestamp": datetime.utcnow().isoformat(),
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

        with open(f"{MODEL_DIR}/{ticker}_{datetime.utcnow().date()}.pkl", "wb") as f:
            pickle.dump(model, f)

        tag = "🪙 PENNY" if is_penny else "💼"
        print(f"[{datetime.utcnow()}] ✅ {ticker} model saved. {tag}")
        return ticker
    except Exception as e:
        print(f"[{datetime.utcnow()}] ❌ {ticker} failed: {e}")
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
        f.write(f"[{datetime.utcnow()}] 📊 Penny trade analysis: {best_str}\n")
    return summary

if __name__ == "__main__":
    tickers = fetch_all_tickers()
    print(f"[{datetime.utcnow()}] 🚀 Starting scan of {len(tickers)} tickers...")

    BATCH_SIZE = 100
    for i in range(0, len(tickers), BATCH_SIZE):
        batch = tickers[i:i + BATCH_SIZE]
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            list(executor.map(process_ticker, batch))
        time.sleep(2)

    manage_models()
    analyze_penny_trades()
