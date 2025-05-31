import yfinance as yf
import pandas as pd
from datetime import datetime
import pickle
import os
import requests
import concurrent.futures
from io import StringIO
import time

MODEL_DIR = "../models"
os.makedirs(MODEL_DIR, exist_ok=True)

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
        df = yf.download(ticker, period="5d", interval="15m", progress=False)
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

        # Skip tiny liquidity
        if avg_volume < 50000:
            return None

        is_penny = latest_price < 5.00

        df["Return"] = df["Close"].pct_change()
        avg_return = df["Return"].mean()
        volatility = df["Return"].std()

        model = {
            "ticker": ticker,
            "timestamp": datetime.utcnow().isoformat(),
            "avg_return": avg_return,
            "volatility": volatility,
            "is_penny": is_penny,
            "price": latest_price,
            "avg_volume": avg_volume
        }

        with open(f"{MODEL_DIR}/{ticker}_{datetime.utcnow().date()}.pkl", "wb") as f:
            pickle.dump(model, f)

        tag = "🪙 PENNY" if is_penny else "💼"
        print(f"[{datetime.utcnow()}] ✅ {ticker} model saved. {tag}")
        return ticker
    except Exception as e:
        print(f"[{datetime.utcnow()}] ❌ {ticker} failed: {e}")
        return None

tickers = fetch_all_tickers()
print(f"[{datetime.utcnow()}] 🚀 Starting scan of {len(tickers)} tickers...")

BATCH_SIZE = 100
for i in range(0, len(tickers), BATCH_SIZE):
    batch = tickers[i:i + BATCH_SIZE]
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        list(executor.map(process_ticker, batch))
    time.sleep(2)

if __name__ == "__main__":
    tickers = fetch_all_tickers()
    for t in tickers[:10]:
        process_ticker(t)
