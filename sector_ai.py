import random

SECTORS = ["Tech", "Energy", "Healthcare", "Financials", "Consumer", "Industrials"]


def get_sector_analysis():
    """Return sector allocation metrics with a suggested decision."""
    results = []
    for sector in SECTORS:
        confidence = round(random.uniform(0.3, 0.9), 2)
        win_rate = round(random.uniform(0.4, 0.8), 2)
        news_score = round(random.uniform(-1, 1), 2)
        decision = "OVERWEIGHT" if confidence > 0.65 and news_score > 0 else "NEUTRAL"
        results.append({
            "Sector": sector,
            "Confidence": confidence,
            "Win Rate": win_rate,
            "News Score": news_score,
            "Decision": decision,
        })
    return results
