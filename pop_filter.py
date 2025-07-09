def filter_by_pop(chain, min_pop=0.70):
    return [c for c in chain if c['pop'] > min_pop]
