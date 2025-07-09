def should_roll(pnl_pct, dte):
    return pnl_pct >= 0.5 or dte < 2

def roll_contract(symbol):
    print(f'\U0001F501 Rolling {symbol} for continued premium...')
