from datetime import datetime, timezone
import os

JOURNAL_PATH = "../logs/trade_journal.md"
os.makedirs("../logs", exist_ok=True)

def journal_trade(ticker, reason, pnl, confidence):
    entry = (
        f"- {ticker} | PnL: {pnl:+.2f} | Confidence: {confidence:.2f}\n"
        f"  Reason: {reason}\n"
    )
    with open(JOURNAL_PATH, "a") as f:
        f.write(f"[{datetime.now(timezone.utc)}] \n{entry}\n")

if __name__ == "__main__":
    journal_trade("TSLA", "Oversold bounce", 50, 0.84)
    print("Journal updated")
