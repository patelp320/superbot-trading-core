"""Automatically retrain models if recent performance drops."""
import pandas as pd

from self_trainer import retrain_model


def scan_and_retrain() -> None:
    """Trigger retraining for strategies with low win rate."""
    df = pd.read_csv("logs/trade_log.csv")
    strategies = df["Strategy"].unique()

    for strat in strategies:
        sub = df[df["Strategy"] == strat].tail(20)
        win_rate = (sub["PnL"] > 0).mean()
        if win_rate < 0.4:
            print(f"[RETRAIN] Strategy {strat} under 40% → retraining model...")
            retrain_model("logs/trade_log.csv")


if __name__ == "__main__":  # pragma: no cover - manual run
    scan_and_retrain()
