def walk_forward(strategy_fn, data, window=60):
    results = []
    for i in range(len(data) - window):
        slice_ = data[i : i + window]
        results.append(strategy_fn(slice_))
    return results
