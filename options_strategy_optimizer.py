"""
AI-powered options optimizer that selects contracts with highest reward/risk ratio and 90%+ win probability.
"""


def find_best_options_trade(candidates):
    high_prob = [c for c in candidates if c.get('win_rate', 0) > 0.9 and c.get('reward_risk', 0) > 1.5]
    best = sorted(high_prob, key=lambda x: x['reward_risk'], reverse=True)
    return best[:3]
