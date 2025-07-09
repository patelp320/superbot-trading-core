import yfinance as yf
from datetime import datetime, time as dt_time, timezone
import os
import requests
import pandas as pd

WATCHLIST_FILE = "../logs/penny_watchlist.txt"
if os.path.exists(WATCHLIST_FILE):
    with open(WATCHLIST_FILE) as f:
        tickers = [line.strip() for line in f if line.strip()]
else:
    tickers = ["GFAI", "MULN", "SOUN"]  # default tickers

high_short_interest = {"GFAI": 0.25, "MULN": 0.30, "SOUN": 0.28}
log_file = "../logs/penny_trades.log"
os.makedirs("../logs", exist_ok=True)

def check_entry(df):
    """Return True if opening range breakout with VWAP reclaim and volume spike."""
    try:
        df = df.between_time("09:30", "10:00")
        if df.empty:
            return False
        open_range_high = df.iloc[:5]['High'].max()
        recent = df.iloc[-1]
        vwap = (df['Close'] * df['Volume']).cumsum() / df['Volume'].cumsum()
        vwap_price = vwap.iloc[-1]
        vol_spike = recent['Volume'] > df['Volume'].mean() * 1.5
        return recent['Close'] > open_range_high and recent['Close'] > vwap_price and vol_spike
    except Exception:
        return False

def score(df):
    try:
        vol = df['Volume'].iloc[-1].item()
        avg_vol = df['Volume'].iloc[-10:].mean().item()
        price_move = ((df['Close'].iloc[-1] - df['Open'].iloc[-1]) / df['Open'].iloc[-1]).item()
        return vol / avg_vol, price_move
    except:
        return 0.0, 0.0

def volatility(df):
    return df['Close'].pct_change().std()

def gap_up(ticker):
    try:
        data = yf.download(ticker, period="2d", interval="1d", prepost=True, progress=False)
        if len(data) < 2:
            return 0.0
        prev_close = data['Close'].iloc[-2]
        today_open = data['Open'].iloc[-1]
        return (today_open - prev_close) / prev_close
    except Exception:
        return 0.0

def sentiment(ticker):
    try:
        resp = requests.get(f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?modules=summaryDetail", timeout=5)
        if resp.ok and 'message' not in resp.text:
            return 0.1
    except Exception:
        pass
    return 0.0

def run():
    """Execute the penny stock scanning routine."""
    with open(log_file, "a") as log:
        for ticker in tickers:
            try:
                df = yf.download(ticker, period="1d", interval="1m", progress=False)
                if df.empty:
                    continue

                vol_score, price_jump = score(df)
                vol = volatility(df)
                gap = gap_up(ticker)
                sent = sentiment(ticker)
                short_int = high_short_interest.get(ticker, 0)

                rel_vol = vol_score

                if rel_vol > 2.0 and price_jump > 0.03 and vol > 0.02:
                    if gap > 0.05 or short_int > 0.25 or sent > 0.05:
                        if check_entry(df):
                            msg = (
                                f"[{datetime.now(timezone.utc)}] 🚀 {ticker} breakout! "
                                f"Volume: {round(vol_score, 1)}x | Move: +{round(price_jump * 100, 2)}%\n"
                            )
                            print(msg.strip())
                            log.write(msg)
            except Exception as e:
                print(f"[{datetime.now(timezone.utc)}] ⚠️ {ticker} failed: {e}")


if __name__ == "__main__":
    run()
    print("[PENNY AI] Module ready for direct use.")
