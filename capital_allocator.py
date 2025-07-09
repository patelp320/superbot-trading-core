# capital_allocator.py

def allocate_capital(equity, confidence, volatility, strategy_weight=1.0):
    weight = (confidence * strategy_weight) / (volatility + 1e-6)
    fraction = min(1.0, weight / 10)  # Normalize
    capital = round(equity * fraction, 2)

    print(f"[ALLOCATOR] Equity={equity}, Allocated=${capital}")
    return capital
