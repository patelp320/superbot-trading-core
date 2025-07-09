"""Visualize open positions and PnL."""
import pandas as pd
import matplotlib.pyplot as plt


def visualize_portfolio():
    """Plot portfolio exposure by sector and compute unrealized PnL."""
    df = pd.read_csv("logs/positions.csv")
    sector_exposure = df.groupby("Sector")["Value"].sum()
    pnl = df["UnrealizedPnL"].sum()

    print(f"[PORTFOLIO] Net PnL: ${pnl:.2f}")

    fig, ax = plt.subplots()
    sector_exposure.plot(kind="barh", color="skyblue", ax=ax)
    ax.set_title("Sector Exposure")
    ax.set_xlabel("Value")
    plt.tight_layout()
    return fig, pnl


if __name__ == "__main__":  # pragma: no cover - manual run
    visualize_portfolio()
