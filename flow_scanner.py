def scan_unusual(options_data):
    return [o for o in options_data if o['volume'] > o['oi'] * 2 and o['oi'] > 500]
