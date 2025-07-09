"""
Dynamically sizes position based on signal quality score and available capital.
"""

def size_position(capital, signal_strength, base_risk=0.01):
    multiplier = min(max(signal_strength, 0.5), 2.0)
    return round(capital * base_risk * multiplier, 2)
