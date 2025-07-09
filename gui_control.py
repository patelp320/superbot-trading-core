import streamlit as st
import json
import os
import time
from datetime import datetime

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import yfinance as yf

from sector_ai import get_sector_analysis
from performance_tracker import summary
from alpha_discovery import discover_tickers
from compliance_guard import is_blocked
from auto_updater import run_update
from strategy_mutator import mutate_all

st.set_page_config(page_title="Superbot Control", layout="wide")

st.title("\U0001F4BB Superbot Control Panel")

# Module status overview
st.subheader("\U0001F4E6 Module Status")
if os.path.exists("log_status.json"):
    with open("log_status.json") as f:
        status = json.load(f)
        st.write("Last Module Completed:", status.get("last_module", "unknown"))
        st.write("Time:", time.ctime(os.path.getmtime("log_status.json")))

# Real-Time price feed
st.subheader("\U0001F4C9 Real-Time Price Feed")
ticker_live = st.text_input("Enter ticker for live price:")
if st.button("Get Live Price"):
    try:
        data = yf.Ticker(ticker_live)
        hist = data.history(period="1d", interval="1m")
        current = hist["Close"].iloc[-1]
        pct_5min = (current - hist["Close"].iloc[-6]) / hist["Close"].iloc[-6] * 100
        pct_15min = (current - hist["Close"].iloc[-16]) / hist["Close"].iloc[-16] * 100
        st.metric("Current Price", f"${current:.2f}")
        st.metric("5 min %", f"{pct_5min:.2f}%")
        st.metric("15 min %", f"{pct_15min:.2f}%")
    except Exception as e:
        st.error(f"Failed to fetch price: {e}")

# Sector allocation and sentiment
st.subheader("\U0001F4CA Sector Allocation Overview")
sector_data = get_sector_analysis()
df_sectors = pd.DataFrame(sector_data)
st.dataframe(df_sectors, use_container_width=True)

st.subheader("\U0001F4F0 Sector News Sentiment")
fig, ax = plt.subplots()
plt.bar(df_sectors["Sector"], df_sectors["News Score"], color="green")
st.pyplot(fig)

# Trade reason log
st.subheader("\U0001F9E0 Trade Reason Log")
try:
    ann = pd.read_csv("logs/annotation_log.csv", names=["Time", "Ticker", "Strategy", "Conf", "Reason"])
    st.dataframe(ann.tail(10), use_container_width=True)
except Exception:
    st.warning("No annotations found yet.")

# Live trade history table
st.subheader("\U0001F4C3 Live Trade History")
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

# Real-time PnL display
try:
    df = pd.read_csv("logs/trade_log.csv")
    today = datetime.now().date()
    pnl = df[pd.to_datetime(df["Date"]).dt.date == today]["PnL"].sum()
    pnl_color = "\U0001F7E2" if pnl >= 0 else "\U0001F534"
    st.metric("Live PnL Today", f"${pnl:.2f}", delta_color="inverse")
    st.markdown(f"{pnl_color} Profit/Loss Stream")
except Exception:
    pass

# Manual strategy test
st.subheader("\U0001F9EA Manual Strategy Test")
selected_test = st.text_input("Enter ticker to test (simulated):")
if st.button("Run Strategy Test"):
    import strategy_writer
    strategy_writer.run()
    st.success(f"Test logic run for {selected_test} (simulated)")

# Strategy performance heatmap
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

# Mode switch for paper/live trading
st.subheader("⚙️ Trading Mode")
mode = st.radio("Select mode:", ["paper", "live"])
if st.button("Save Mode"):
    with open("config.json", "w") as f:
        json.dump({"mode": mode}, f)
    st.success(f"✅ Mode saved: {mode}")

# PnL summary from performance tracker
st.subheader("💰 PnL Summary")
summary()

# Strategy and model reload controls
st.subheader("🔄 Refresh Core")
if st.button("Run Auto Updater"):
    run_update()
    st.success("✅ Updated models & strategies")

if st.button("Mutate Strategies"):
    mutate_all()
    st.success("✅ Mutation complete")

# Alpha discovery suggestions
st.subheader("📈 Alpha Discovery")
if st.button("Discover Tickers"):
    tickers = discover_tickers()
    st.write("Suggested:", tickers)

# Compliance check helper
st.subheader("🔒 Compliance Check")
ticker_check = st.text_input("Enter ticker to check")
price = st.number_input("Price", value=1.0)
days = st.slider("Option expiry in days", 0, 30, 7)
if st.button("Check Compliance"):
    if is_blocked(ticker_check.upper(), price, days):
        st.error("❌ Trade Blocked")
    else:
        st.success("✅ Trade Allowed")

# Strategy audit utilities
st.subheader("\U0001F4DA Strategy Audit")
if st.button("Audit Strategies"):
    import strategy_auditor
    strategy_auditor.audit_strategies()
    st.success("\u2705 Strategy version log updated.")

# Portfolio visualization
st.subheader("\U0001F4C8 Portfolio Visualizer")
if st.button("Show Portfolio"):
    from portfolio_visualizer import visualize_portfolio
    fig, pnl = visualize_portfolio()
    st.pyplot(fig)
    st.metric("Unrealized PnL", f"${pnl:.2f}")

# Interactive backtesting
st.subheader("\U0001F9E6 Run Interactive Backtest")
ticker_bt = st.text_input("Ticker")
strat_bt = st.text_input("Strategy (e.g., alpha_1699889932)")
start_bt = st.date_input("Start")
end_bt = st.date_input("End")
if st.button("Run Backtest"):
    from interactive_backtester import run_backtest
    result = run_backtest(ticker_bt, strat_bt, str(start_bt), str(end_bt))
    st.write(result)

# Adaptive retraining trigger
st.subheader("\U0001F501 Auto-Retrain Trigger")
if st.button("Run Adaptive Retrainer"):
    from adaptive_retrainer import scan_and_retrain
    scan_and_retrain()
    st.success("\u2705 Retraining triggered if needed.")
