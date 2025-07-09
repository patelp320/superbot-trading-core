"""
Watches equity curve performance and triggers pause signals if drawdown exceeds threshold.
"""

def monitor_equity_curve(equity_history, max_drawdown_pct=0.15):
    if not equity_history:
        return False
    peak = max(equity_history)
    current = equity_history[-1]
    drawdown = (peak - current) / peak
    if drawdown > max_drawdown_pct:
        print(f"⚠️ Drawdown alert: {drawdown:.2%} exceeded max of {max_drawdown_pct:.2%}")
        return True
    return False
