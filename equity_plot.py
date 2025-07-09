import os
import pandas as pd
import matplotlib.pyplot as plt

LOG_DIR = os.environ.get("LOG_DIR", "logs")
DATA_PATH = os.path.join(LOG_DIR, "trade_journal.csv")

def plot_equity_curve() -> None:
    os.makedirs(LOG_DIR, exist_ok=True)
    if not os.path.exists(DATA_PATH):
        print("Trade journal not found")
        return
    df = pd.read_csv(DATA_PATH)
    if "PnL" not in df.columns or "Date" not in df.columns:
        print("Missing columns in trade journal")
        return
    df["cum_pnl"] = df["PnL"].cumsum()
    plt.figure()
    plt.plot(df["Date"], df["cum_pnl"])
    plt.title("Equity Curve")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(LOG_DIR, "equity_curve.png"))

if __name__ == "__main__":
    plot_equity_curve()
