def scan_gaps(tickers):
    return [t for t in tickers if gapped_up(t) and has_news(t)]

def gapped_up(t):
    return True  # placeholder

def has_news(t):
    return True  # add news check here
