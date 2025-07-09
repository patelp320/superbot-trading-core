import pandas as pd
import matplotlib.pyplot as plt

DATA_PATH = "logs/trade_journal.csv"

def plot_equity_curve():
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
    plt.savefig("logs/equity_curve.png")

if __name__ == "__main__":
    plot_equity_curve()
