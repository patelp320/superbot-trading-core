import random


def check_darkpool(ticker):
    avg_volume = random.randint(100000, 200000)
    current_volume = avg_volume * random.uniform(1.0, 3.5)

    if current_volume > avg_volume * 2:
        print(f"[DARKPOOL] 🚨 Accumulation spotted: {ticker} @ {int(current_volume)}")
        return True
    else:
        print(f"[DARKPOOL] Normal volume: {ticker}")
        return False
