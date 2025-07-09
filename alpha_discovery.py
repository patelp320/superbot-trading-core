import random


def discover_tickers():
    universe = ["TSLA", "GFAI", "NVDA", "SNTI", "COSM", "META", "AMD", "MSFT", "RIVN", "SPY"]
    picks = random.sample(universe, 10)

    with open("alpha_candidates.txt", "w") as f:
        for t in picks:
            f.write(t + "\n")

    print(f"[ALPHA DISCOVERY] ✅ Suggested tickers: {picks}")
    return picks
