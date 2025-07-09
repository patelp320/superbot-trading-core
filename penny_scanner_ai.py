import yfinance as yf
import pandas as pd
import requests
from datetime import datetime, timezone
import json


def score_ticker(gap, vol_rel, float_mil, has_news):
    score = 0
    score += gap * 1.5
    score += vol_rel * 10
    score += (50 - float_mil) * 1.2
    score += 25 if has_news else 0
    return round(score, 2)


def fetch_float(ticker):
    try:
        r = requests.get(f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?modules=defaultKeyStatistics", timeout=5)
        if r.ok and 'floatShares' in r.text:
            # naive parsing
            val = [line for line in r.text.splitlines() if 'floatShares' in line][0]
            num = ''.join([c for c in val if c.isdigit()])
            if num:
                return float(num) / 1e6
    except Exception:
        pass
    return 100.0


def news_catalyst(ticker):
    try:
        r = requests.get(f"https://query1.finance.yahoo.com/v1/finance/search?q={ticker}", timeout=5)
        if r.ok:
            text = r.text.lower()
            if 'upgrade' in text or 'approval' in text or 'contract' in text:
                return True
    except Exception:
        pass
    return False


TICKERS = ["GFAI", "SNTI", "COSM"]

results = []
for ticker in TICKERS:
    try:
        df = yf.download(ticker, period="2d", interval="1d", prepost=True, progress=False)
        if df.empty:
            continue
        if len(df) < 2:
            continue
        prev_close = df['Close'].iloc[-2]
        open_today = df['Open'].iloc[-1]
        gap = round((open_today - prev_close) / prev_close * 100, 2)
        intraday = yf.download(ticker, period="1d", interval="1m", prepost=True, progress=False)
        if intraday.empty:
            continue
        today_vol = intraday['Volume'].sum()
        avg_vol = df['Volume'].iloc[-2]
        vol_rel = round(today_vol / avg_vol, 2) if avg_vol else 0
        price = intraday['Close'].iloc[-1]
        if price > 5:
            continue
        float_mil = fetch_float(ticker)
        has_news = news_catalyst(ticker)
        if gap < 4 or vol_rel < 2 or float_mil > 50:
            continue
        score = score_ticker(gap, vol_rel, float_mil, has_news)
        results.append({
            'ticker': ticker,
            'gap': gap,
            'float': float_mil,
            'vol_rel': vol_rel,
            'news': 'yes' if has_news else 'no',
            'score': score
        })
    except Exception as e:
        print(f"[{datetime.now(timezone.utc)}] ❌ {ticker} scan failed: {e}")

results.sort(key=lambda x: x['score'], reverse=True)
print(json.dumps(results, indent=2))
