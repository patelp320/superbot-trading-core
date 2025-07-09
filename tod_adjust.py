def get_aggression(now):
    return 'high' if 9 <= now.hour < 10 else 'low'
