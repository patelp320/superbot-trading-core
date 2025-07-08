import smtplib, os
from datetime import datetime
from email.mime.text import MIMEText

EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")

def last_trades(path, n=5):
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return f.readlines()[-n:]

def error_summary(path):
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return [l for l in f.readlines() if "❌" in l][-5:]

trades = last_trades('../logs/fake_trades.log')
errors = error_summary('../logs/learn.log')
watchlist = ["AAPL", "TSLA", "SPY"]
strategy_perf = last_trades('../logs/strategy_performance.log')
penny_log = '../logs/penny_trade_log.csv'

def penny_summary(path):
    if not os.path.exists(path):
        return "No trades"
    import pandas as pd
    df = pd.read_csv(path, names=["Ticker", "Entry", "Exit", "Strategy", "Pct"], header=None)
    winners = df[df['Pct'] > 0]
    losers = df[df['Pct'] <= 0]
    win_rate = round(len(winners) / len(df) * 100, 2) if len(df) else 0
    avg_win = round(winners['Pct'].mean(), 2) if not winners.empty else 0
    avg_loss = round(losers['Pct'].mean(), 2) if not losers.empty else 0
    return f"Trades: {len(df)} | WinRate: {win_rate}% | AvgWin: {avg_win}% | AvgLoss: {avg_loss}%"

# Report summary
summary = f"""
📊 Superbot AI Status – {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC

✅ Models trained: {len(os.listdir('../models'))}
📂 Logs recorded: {len(os.listdir('../logs'))}
Top Trades:\n{''.join(trades)}
Tomorrow Watchlist: {', '.join(watchlist)}
Strategy Scores:\n{''.join(strategy_perf)}
Errors:\n{''.join(errors)}
Penny Summary: {penny_summary(penny_log)}
"""

msg = MIMEText(summary)
msg['Subject'] = "🧠 Superbot Status Report"
msg['From'] = EMAIL_FROM
msg['To'] = EMAIL_TO

try:
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
        print(f"✅ Email sent to {EMAIL_TO}")
except Exception as e:
    print(f"❌ Email failed: {e}")
