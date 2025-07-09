def evaluate(strategy_results):
    return strategy_results.get('sharpe', 0) > 2.0 and strategy_results.get('win_rate', 0) > 0.6
