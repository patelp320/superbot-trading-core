def choose_strike(chain, delta_range):
    return [o for o in chain if delta_range[0] <= o['delta'] <= delta_range[1]]
