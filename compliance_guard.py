BANNED = {"CEI", "HCMC", "BBBYQ"}


def is_blocked(ticker, price=1.00, option_expiry_days=7):
    if ticker in BANNED:
        print(f"🚫 {ticker} is banned")
        return True
    if price < 0.25:
        print(f"⚠️ Penny stock under $0.25 blocked: {ticker}")
        return True
    if option_expiry_days <= 1:
        print(f"⚠️ Option too short-dated for {ticker}")
        return True
    return False
