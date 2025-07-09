"""
Scans hundreds of tickers per second with lightweight filters before deeper analysis.
"""


def rapid_scan(tickers):
    print(f"\u26a1 Rapid scanning {len(tickers)} tickers...")
    return [t for t in tickers if len(t) < 6 and not any(x in t for x in ["$", "-"])]
