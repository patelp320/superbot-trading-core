def staged_exit(price, entry, sold1=False, sold2=False):
    gain = (price - entry) / entry
    if not sold1 and gain >= 0.05:
        return "take_33"
    if not sold2 and gain >= 0.10:
        return "take_66"
    return "hold"
