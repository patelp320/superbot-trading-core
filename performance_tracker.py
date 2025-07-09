import pandas as pd
from datetime import datetime


def summary():
    df = pd.read_csv("logs/trade_log.csv")
    df["Date"] = pd.to_datetime(df["Date"])

    today = datetime.now().date()
    df_today = df[df["Date"].dt.date == today]

    this_week = df[df["Date"] >= pd.Timestamp.today() - pd.Timedelta(days=7)]
    this_month = df[df["Date"].dt.month == today.month]

    print(f"[PERFORMANCE] Today: ${df_today['PnL'].sum():.2f}")
    print(f"[PERFORMANCE] Last 7 days: ${this_week['PnL'].sum():.2f}")
    print(f"[PERFORMANCE] Month: ${this_month['PnL'].sum():.2f}")
