import random


def scan_orderbook(ticker):
    bids = [random.randint(100, 2000) for _ in range(10)]
    asks = [random.randint(100, 2000) for _ in range(10)]

    total_bid = sum(bids)
    total_ask = sum(asks)
    spoof_flag = total_bid > total_ask * 3 or total_ask > total_bid * 3

    print(f"[ORDERBOOK] {ticker} B:{total_bid} A:{total_ask}")
    if spoof_flag:
        print("⚠️ Spoofing or wall detected!")
    return {"bid": total_bid, "ask": total_ask, "spoof": spoof_flag}
