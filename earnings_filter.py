def filter_out_earnings(chain):
    return [c for c in chain if not c['earnings_this_week']]
