"""
Generates a summary of trades and PnL for reporting purposes.
"""

def generate_daily_summary(trades):
    print("\U0001F4C8 Daily Summary:")
    total_profit = sum(t['pnl'] for t in trades)
    for t in trades:
        print(f"- {t['symbol']} | PnL: ${t['pnl']:.2f}")
    print(f"\nTotal PnL: ${total_profit:.2f}")
