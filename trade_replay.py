# trade_replay.py
import pandas as pd


def replay_trades(log_path, new_strategy):
    df = pd.read_csv(log_path)
    for _, row in df.iterrows():
        features = [row["Confidence"], row["Volume"], row["Volatility"]]
        pred = new_strategy.predict([features])[0]

        if pred > 0.5 and row["PnL"] <= 0:
            print(f"\U0001F4A1 Missed alpha: {row['Ticker']} | Old PnL: {row['PnL']}")
