def should_roll(position):
    return position.days_to_expiry() < 3 or position.is_in_the_money()


def roll(position):
    print(f"Rolling {position.symbol} to next expiry...")
