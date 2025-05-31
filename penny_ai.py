import yfinance as yf
from datetime import datetime
import os

tickers = ["GFAI", "MULN", "SOUN"]  # Delisted ones removed
log_file = "../logs/penny_trades.log"
os.makedirs("../logs", exist_ok=True)

def score(df):
    try:
        vol = df['Volume'].iloc[-1].item()
        avg_vol = df['Volume'].iloc[-10:].mean().item()
        price_move = ((df['Close'].iloc[-1] - df['Open'].iloc[-1]) / df['Open'].iloc[-1]).item()
        return vol / avg_vol, price_move
    except:
        return 0.0, 0.0

with open(log_file, "a") as log:
    for ticker in tickers:
        try:
            df = yf.download(ticker, period="1d", interval="5m", progress=False)
            if df.empty:
                continue

            vol_score, price_jump = score(df)
            if vol_score > 3.0 and price_jump > 0.03:
                msg = f"[{datetime.utcnow()}] 🚀 {ticker} breakout! Volume: {round(vol_score, 1)}x | Move: +{round(price_jump * 100, 2)}%\n"
                print(msg.strip())
                log.write(msg)
        except Exception as e:
            print(f"[{datetime.utcnow()}] ⚠️ {ticker} failed: {e}")


if __name__ == "__main__":
    print("[PENNY AI] Module ready for direct use.")
