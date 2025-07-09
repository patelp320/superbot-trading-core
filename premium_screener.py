# premium_screener.py
import random


def screen_premium_candidates(tickers):
    results = []
    for t in tickers:
        premium = round(random.uniform(1.0, 10.0), 2)
        iv_rank = round(random.uniform(0.3, 1.0), 2)
        score = premium * iv_rank
        results.append((t, score))

    top = sorted(results, key=lambda x: x[1], reverse=True)[:5]
    print(f"[PREMIUM] Top Premium Candidates: {top}")
    return top
