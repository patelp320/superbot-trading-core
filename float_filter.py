def is_explosive(float_shares, volatility):
    return float_shares < 10_000_000 and volatility > 0.05
