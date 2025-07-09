import os
from datetime import datetime, timezone
import random
from ai_modules.ai_stop_loss_manager import trailing_stop
from execution.position_sizer import size_position
from execution.trade_logger import log_trade
from broker_failover import choose_broker
from market_anomaly_detector import check_anomalies


def place_order(signal, size):
    """Placeholder for real brokerage API order placement."""
    price = signal.get("price", signal.get("premium", 0))
    executed_price = round(price * random.uniform(0.99, 1.01), 2)
    return executed_price

log_file = "../logs/fake_trades.log"
penny_log = "../logs/penny_trade_log.csv"
os.makedirs("../logs", exist_ok=True)

capital = 10000.0
daily_pnl = 0.0
max_drawdown = -200.0
open_positions = 0
max_positions = 5
margin_limit = capital * 2
used_margin = 0.0

# Mock trade signal (normally fed by options_ai or penny_ai)
mock_signals = [
    {"ticker": "TSLA", "strategy": "CSP", "action": "sell_put", "strike": 150, "premium": 2.25},
    {"ticker": "GFAI", "strategy": "Gap & Go", "action": "buy_stock", "qty": 100, "price": 2.17, "exit": 2.35},
    {"ticker": "SNTI", "strategy": "VWAP reclaim", "action": "buy_stock", "qty": 1000, "price": 0.91, "exit": 1.10},
    {"ticker": "COSM", "strategy": "Low float run", "action": "buy_stock", "qty": 200, "price": 4.88, "exit": 6.12},
    {"ticker": "NVDA", "strategy": "call_spread", "action": "open_spread", "details": "280/290"}
]

broker = choose_broker()
print(f"[{datetime.now(timezone.utc)}] Using broker {broker}")
flagged = check_anomalies([s["ticker"] for s in mock_signals])

with open(log_file, "a") as f:
    for signal in mock_signals:
        if signal["ticker"] in flagged:
            print(f"[{datetime.now(timezone.utc)}] ⚠️ {signal['ticker']} suspended due to anomaly")
            continue
        if open_positions >= max_positions:
            print(f"[{datetime.now(timezone.utc)}] 🚫 Max positions reached. Skipping {signal['ticker']}")
            continue
        price = signal.get("price", signal.get("premium", 0))
        qty = signal.get("qty", 1)
        confidence = random.uniform(0.5, 1.0)
        size = size_position(capital, 0.02, confidence)
        cost = min(price * qty, size)

        if used_margin + abs(cost) > margin_limit:
            print(f"[{datetime.now(timezone.utc)}] ⚠️ Margin limit reached. Skipping {signal['ticker']}")
            continue

        executed_price = place_order(signal, size)
        exit_price = signal.get("exit")
        if exit_price:
            pnl = (exit_price - price) * signal.get("qty", 1)
        else:
            pnl = random.uniform(-0.05, 0.05) * cost
        used_margin += abs(cost)
        daily_pnl += pnl
        stop = trailing_stop(executed_price, random.uniform(0.5, 2))
        open_positions += 1

        msg = (
            f"[{datetime.now(timezone.utc)}] 💡 Simulated trade: {signal['action']} on {signal['ticker']} | "
            f"Strategy: {signal['strategy']} | Filled at: ${executed_price} | PnL: {round(pnl,2)} | Stop: {stop}"
        )
        print(msg)
        f.write(msg + "\n")
        log_trade(msg)
        if signal.get("price", 0) < 5:
            with open(penny_log, "a") as pf:
                pf.write(f"{signal['ticker']},{signal.get('price')},{exit_price},{signal['strategy']},{round((pnl / (signal.get('price') * signal.get('qty',1))) * 100,2) if exit_price else ''}\n")

        if daily_pnl < max_drawdown:
            print(f"[{datetime.now(timezone.utc)}] 🛑 Max drawdown reached. Halting trades.")
            break

if __name__ == "__main__":
    print("[SIM] Fake trade simulation completed.")
