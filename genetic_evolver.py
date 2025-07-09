def evolve(strategies):
    mutated = []
    for s in strategies:
        mutated.append(s + "_mut")
    return mutated
