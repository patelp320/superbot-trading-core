"""
Filters trades based on adaptive criteria like volatility, market regime, and AI predictions.
"""


def filter_trades(trades, market_volatility):
    threshold = 0.6 if market_volatility > 0.3 else 0.4
    return [t for t in trades if t['ai_score'] > threshold]
