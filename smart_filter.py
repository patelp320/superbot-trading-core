def is_trade_ok(macro, vix, news, conf):
    return macro == "bullish" and vix < 20 and news > 0.5 and conf > 0.85
