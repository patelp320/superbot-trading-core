from datetime import datetime, timezone


def log_trade(msg: str, path: str = "../logs/trades.log"):
    with open(path, "a") as f:
        f.write(f"[{datetime.now(timezone.utc)}] {msg}\n")
