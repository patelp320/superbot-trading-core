"""
Limits trade frequency during high volatility or when win rate drops to preserve capital.
"""


def throttle_decision(win_rate, trade_count, max_trades=10):
    if win_rate < 0.7 or trade_count >= max_trades:
        print("\ud83d\udded Throttle triggered: Waiting for better setup.")
        return True
    return False
