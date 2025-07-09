"""Disable poorly performing strategies based on recent results."""

from pathlib import Path

import pandas as pd

DISABLED_FILE = "disabled_strategies.txt"


def check_kill_switch(log_path: str) -> None:
    """Disable strategies with low win rate or negative average PnL."""
    df = pd.read_csv(log_path)
    strategies = df["Strategy"].unique()
    out_path = Path(DISABLED_FILE)

    with out_path.open("w") as f:
        for strategy in strategies:
            recent = df[df["Strategy"] == strategy].tail(10)
            win_rate = (recent["PnL"] > 0).mean()
            avg_pnl = recent["PnL"].mean()
            if win_rate < 0.4 or avg_pnl < 0:
                f.write(f"{strategy}\n")
                print(f"\u26a0\ufe0f Strategy {strategy} disabled")
