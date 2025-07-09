"""
Dynamically sizes position based on signal quality score and available capital.
"""

def size_position(capital, signal_strength, base_risk=0.01):
    multiplier = min(max(signal_strength, 0.5), 2.0)
    return round(capital * base_risk * multiplier, 2)


def position_size(confidence, volatility, equity=10000, max_risk=0.02):
    """Return position size based on confidence and volatility."""
    risk_per_trade = equity * max_risk
    weight = confidence / (volatility + 1e-6)
    size = int(risk_per_trade * weight)
    return max(1, size)
