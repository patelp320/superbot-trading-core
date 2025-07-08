import os
from datetime import datetime
import random

log_file = "../logs/fake_trades.log"
os.makedirs("../logs", exist_ok=True)

# Mock trade signal (normally fed by options_ai or penny_ai)
mock_signals = [
    {"ticker": "TSLA", "strategy": "CSP", "action": "sell_put", "strike": 150, "premium": 2.25},
    {"ticker": "GFAI", "strategy": "scalp", "action": "buy_stock", "qty": 100, "price": 2.15},
    {"ticker": "NVDA", "strategy": "call_spread", "action": "open_spread", "details": "280/290"}
]

with open(log_file, "a") as f:
    for signal in mock_signals:
        executed_price = round(signal.get("price", signal.get("premium", 0)) * random.uniform(0.98, 1.02), 2)
        msg = f"[{datetime.utcnow()}] 💡 Simulated trade: {signal['action']} on {signal['ticker']} | Strategy: {signal['strategy']} | Filled at: ${executed_price}"
        print(msg)
        f.write(msg + "\n")

if __name__ == "__main__":
    print("[SIM] Fake trade simulation completed.")
