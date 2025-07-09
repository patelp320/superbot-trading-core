def select_short_dte(chain):
    return [c for c in chain if 6 <= c['dte'] <= 10]
