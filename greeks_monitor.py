import random


def get_greeks(symbol: str):
    """Return option greeks for the given symbol. Placeholder for IBKR API."""
    greeks = {
        "delta": round(random.uniform(-1, 1), 2),
        "gamma": round(random.uniform(0, 1), 2),
        "theta": round(random.uniform(-1, 0), 2),
        "vega": round(random.uniform(0, 1), 2),
    }
    print(f"[GREEKS] {symbol}: {greeks}")
    return greeks
