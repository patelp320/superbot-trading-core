# log_dashboard.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("\U0001F4CA Superbot Trade Log Dashboard")

df = pd.read_csv("logs/trade_log.csv")

st.subheader("Daily PnL")
daily = df.groupby("Date")["PnL"].sum()
st.line_chart(daily)

st.subheader("Strategy Win Rates")
win_rate = df[df["PnL"] > 0].groupby("Strategy").size() / df.groupby("Strategy").size()
st.bar_chart(win_rate.fillna(0))
