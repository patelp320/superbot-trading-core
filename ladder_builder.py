def build_ladder(symbol, base_strike, count=3):
    return [f"{symbol}_{base_strike + 5*i}_C" for i in range(count)]
