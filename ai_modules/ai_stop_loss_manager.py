from datetime import datetime, timedelta, timezone
import random


def trailing_stop(entry_price: float, atr: float) -> float:
    """Calculate trailing stop based on ATR."""
    return round(entry_price - 2 * atr, 2)


def time_stop(entry_time: datetime, max_hours: int = 4) -> bool:
    return datetime.now(timezone.utc) - entry_time > timedelta(hours=max_hours)


def example_usage():
    price = 100.0
    atr = random.uniform(1, 3)
    ts = trailing_stop(price, atr)
    exit_now = time_stop(datetime.now(timezone.utc) - timedelta(hours=5))
    print(f"ATR {atr:.2f} -> trailing stop {ts}; time exit: {exit_now}")


if __name__ == "__main__":
    example_usage()
