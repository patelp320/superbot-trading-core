from datetime import datetime, timezone
import os
import csv

JOURNAL_DIR = "../logs"
os.makedirs(JOURNAL_DIR, exist_ok=True)


def journal_trade(symbol: str, strategy: str, fill: float, pnl: float, stop: float) -> None:
    """Append a trade entry to a dated CSV journal."""
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    path = os.path.join(JOURNAL_DIR, f"trade_journal_{date_str}.csv")
    file_exists = os.path.exists(path)
    with open(path, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["time", "symbol", "strategy", "fill", "PnL", "stop"])
        writer.writerow([
            datetime.now(timezone.utc).isoformat(),
            symbol,
            strategy,
            fill,
            pnl,
            stop,
        ])

if __name__ == "__main__":
    journal_trade("TSLA", "Oversold bounce", 10.5, 50, 8.0)
    print("Journal updated")
