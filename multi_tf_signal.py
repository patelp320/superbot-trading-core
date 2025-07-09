def is_confirmed(symbol): return all([check_tf(symbol, tf) for tf in ['1m', '5m', '1h', '1d']])
def check_tf(symbol, tf): return True  # placeholder for real TA
