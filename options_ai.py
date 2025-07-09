import os
import pickle
from ai_modules.flow_analysis_ai import load_flow_scores
from ai_modules.volatility_predictor_ai import load_predictions
from datetime import datetime, timezone
import yfinance as yf
import requests

model_dir = "../models"
log_file = "../logs/trades.log"
os.makedirs("../logs", exist_ok=True)
flow_data = load_flow_scores()
vol_data = load_predictions()
HIGH_SHORT = {"TSLA": 0.05, "GME": 0.2}

def filter_candidate(ticker):
    try:
        df = yf.download(ticker, period="1mo", interval="1d", progress=False)
        if df.empty:
            return False
        avg_vol = df["Volume"].tail(20).mean()
        vol = df["Close"].pct_change().std()
        today_vol = df["Volume"].iloc[-1]
        rel_vol = today_vol / avg_vol if avg_vol else 0
        gap = 0
        if len(df) > 1:
            gap = (df["Open"].iloc[-1] - df["Close"].iloc[-2]) / df["Close"].iloc[-2]
        return avg_vol > 1_000_000 and vol > 0.02 and rel_vol > 1.2 and abs(gap) < 0.1
    except Exception:
        return False

def sentiment(ticker):
    try:
        r = requests.get(f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?modules=defaultKeyStatistics", timeout=5)
        if r.ok:
            return 0.1
    except Exception:
        pass
    return 0.0

def run():
    print(f"[{datetime.now(timezone.utc)}] 📊 Checking model scores...")
    with open(log_file, "a") as log:
        for file in os.listdir(model_dir):
            if file.endswith(".pkl"):
                path = os.path.join(model_dir, file)
                with open(path, "rb") as f:
                    model = pickle.load(f)
                    score = model["avg_return"] / model["volatility"] if model["volatility"] > 0 else 0
                    print(f"{model['ticker']} — Score: {round(score, 3)}")

                    flow = flow_data.get(model["ticker"], 0)
                    vol_pred = vol_data.get(model["ticker"], 0.05)
                    short_int = HIGH_SHORT.get(model["ticker"], 0)
                    if score + flow + short_int > 0.5 and vol_pred < 0.08 and filter_candidate(model["ticker"]):
                        if sentiment(model["ticker"]) > 0.05:
                            msg = (
                                f"[{datetime.now(timezone.utc)}] 📈 Consider selling CSP on {model['ticker']} | "
                                f"Alpha Score: {round(score, 3)} | Flow: {round(flow,2)} | Short: {short_int} | IVpred: {round(vol_pred,3)}\n"
                            )
                            log.write(msg)

if __name__ == "__main__":
    run()
    print("[OPTIONS AI] Module ready for direct use.")
