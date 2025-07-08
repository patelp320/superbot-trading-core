import os
from datetime import datetime
import random
from ai_modules.ai_stop_loss_manager import trailing_stop

log_file = "../logs/fake_trades.log"
os.makedirs("../logs", exist_ok=True)

capital = 10000.0
daily_pnl = 0.0
max_drawdown = -100.0
margin_limit = capital * 2
used_margin = 0.0

# Mock trade signal (normally fed by options_ai or penny_ai)
mock_signals = [
    {"ticker": "TSLA", "strategy": "CSP", "action": "sell_put", "strike": 150, "premium": 2.25},
    {"ticker": "GFAI", "strategy": "scalp", "action": "buy_stock", "qty": 100, "price": 2.15},
    {"ticker": "NVDA", "strategy": "call_spread", "action": "open_spread", "details": "280/290"}
]

with open(log_file, "a") as f:
    for signal in mock_signals:
        cost = signal.get("price", signal.get("premium", 0)) * signal.get("qty", 1)
        cost = min(cost, capital * 0.02)

        if used_margin + abs(cost) > margin_limit:
            print(f"[{datetime.utcnow()}] ⚠️ Margin limit reached. Skipping {signal['ticker']}")
            continue

        executed_price = round(signal.get("price", signal.get("premium", 0)) * random.uniform(0.98, 1.02), 2)
        pnl = random.uniform(-0.05, 0.05) * cost
        used_margin += abs(cost)
        daily_pnl += pnl
        stop = trailing_stop(executed_price, random.uniform(0.5, 2))

        msg = (
            f"[{datetime.utcnow()}] 💡 Simulated trade: {signal['action']} on {signal['ticker']} | "
            f"Strategy: {signal['strategy']} | Filled at: ${executed_price} | PnL: {round(pnl,2)} | Stop: {stop}"
        )
        print(msg)
        f.write(msg + "\n")

        if daily_pnl < max_drawdown:
            print(f"[{datetime.utcnow()}] 🛑 Max drawdown reached. Halting trades.")
            break

if __name__ == "__main__":
    print("[SIM] Fake trade simulation completed.")
