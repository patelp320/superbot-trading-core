from datetime import datetime


def log_trade(msg: str, path: str = "../logs/trades.log"):
    with open(path, "a") as f:
        f.write(f"[{datetime.utcnow()}] {msg}\n")
