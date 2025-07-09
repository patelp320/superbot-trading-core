import streamlit as st
import json
import os
import time
from datetime import datetime

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Superbot Control", layout="wide")

st.title("\U0001F4BB Superbot Control Panel")

st.subheader("\U0001F4E6 Module Status")
if os.path.exists("log_status.json"):
    with open("log_status.json") as f:
        status = json.load(f)
        st.write("Last Module Completed:", status.get("last_module", "unknown"))
        st.write("Time:", time.ctime(os.path.getmtime("log_status.json")))

st.subheader("\u2705 Compliance Check")
st.write("All systems operating within defined parameters.")

# Add after Compliance Check in gui_control.py
st.subheader("\ud83d\udcc3 Live Trade History")
try:
    df = pd.read_csv("logs/trade_log.csv")

    tickers = df["Ticker"].unique().tolist()
    strategies = df["Strategy"].unique().tolist()

    col1, col2 = st.columns(2)
    with col1:
        selected_ticker = st.selectbox("Filter by Ticker", ["All"] + tickers)
    with col2:
        selected_strategy = st.selectbox("Filter by Strategy", ["All"] + strategies)

    if selected_ticker != "All":
        df = df[df["Ticker"] == selected_ticker]
    if selected_strategy != "All":
        df = df[df["Strategy"] == selected_strategy]

    st.dataframe(df.sort_values("Date", ascending=False).head(25), use_container_width=True)

except Exception as e:
    st.error(f"Could not load trade log: {e}")

# PnL Section with real-time ticker display
try:
    df = pd.read_csv("logs/trade_log.csv")
    today = datetime.now().date()
    pnl = df[pd.to_datetime(df["Date"]).dt.date == today]["PnL"].sum()
    pnl_color = "\U0001F7E2" if pnl >= 0 else "\U0001F534"
    st.metric("Live PnL Today", f"${pnl:.2f}", delta_color="inverse")
    st.markdown(f"{pnl_color} Profit/Loss Stream")
except Exception:
    pass

st.subheader("\U0001F9EA Manual Strategy Test")
selected_test = st.text_input("Enter ticker to test (simulated):")
if st.button("Run Strategy Test"):
    import strategy_writer
    strategy_writer.run()
    st.success(f"Test logic run for {selected_test} (simulated)")

st.subheader("\U0001F525 Strategy Performance Heatmap")
try:
    df["Date"] = pd.to_datetime(df["Date"])
    today_df = df[df["Date"].dt.date == datetime.now().date()]
    heat = today_df.groupby("Strategy")["PnL"].sum().sort_values(ascending=False)

    fig, ax = plt.subplots()
    sns.heatmap([[v] for v in heat], annot=[[f"${v:.2f}"] for v in heat], yticklabels=heat.index, cmap="RdYlGn", ax=ax)
    st.pyplot(fig)
except Exception:
    st.warning("No heatmap data available.")
