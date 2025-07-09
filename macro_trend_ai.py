# macro_trend_ai.py
import random


def get_macro_indicators():
    return {
        "VIX": random.uniform(12, 35),
        "CPI": random.uniform(2.0, 9.0),
        "FedRate": random.uniform(1.0, 5.5)
    }


def compute_macro_score():
    data = get_macro_indicators()
    score = 0

    if data["VIX"] > 25:
        score -= 0.5
    if data["CPI"] > 6:
        score -= 0.3
    if data["FedRate"] > 4:
        score -= 0.2

    macro_score = max(-1, min(1, 1 + score))
    if score <= -1.0:
        print("[MACRO] Warning: High risk across all indicators")
    print(f"[MACRO] Indicators: {data}, Score: {macro_score:.2f}")
    return macro_score
