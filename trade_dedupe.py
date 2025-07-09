cache = set()

def should_trade(symbol):
    if symbol in cache:
        return False
    cache.add(symbol)
    return True
