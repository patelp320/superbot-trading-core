import numpy as np
import pandas as pd


def evaluate_strategy(df: pd.DataFrame, strategy_func, train_size: int = 100, test_size: int = 20):
    """Run walk-forward validation using rolling windows."""
    results = []

    for start in range(0, len(df) - train_size - test_size, test_size):
        train = df.iloc[start : start + train_size]
        test = df.iloc[start + train_size : start + train_size + test_size]

        model = strategy_func(train)
        predictions = model.predict(test)

        pnl = predictions["PnL"]
        sharpe = pnl.mean() / (pnl.std() or 1)
        accuracy = (pnl > 0).mean()

        results.append({"start": start, "accuracy": accuracy, "sharpe": sharpe})

    summary = pd.DataFrame(results)
    print(summary)
    return summary
