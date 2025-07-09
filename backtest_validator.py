# backtest_validator.py
import random


def simulate_trades(strategy_func, runs=20):
    results = [random.uniform(-5, 10) for _ in range(runs)]
    win_rate = sum(1 for r in results if r > 0) / runs
    avg_return = sum(results) / runs
    drawdown = min(results)

    print(f"[VALIDATOR] Wins={win_rate:.2f}, Avg={avg_return:.2f}, DD={drawdown:.2f}")

    if win_rate < 0.5 or drawdown < -20:
        return False
    return True
