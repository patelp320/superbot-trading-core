import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

from sector_ai import get_sector_analysis

st.set_page_config(page_title="Superbot Control Center", layout="wide")

st.title("\U0001F6E0\ufe0f Superbot Control Center")

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

st.subheader("\U0001F4CA Sector Allocation Overview")
sector_data = get_sector_analysis()
df_sectors = pd.DataFrame(sector_data)
st.dataframe(df_sectors, use_container_width=True)

st.subheader("\U0001F4F0 Sector News Sentiment")
fig, ax = plt.subplots()
plt.bar(df_sectors["Sector"], df_sectors["News Score"], color="green")
st.pyplot(fig)

st.subheader("\U0001F9E0 Trade Reason Log")
try:
    ann = pd.read_csv("logs/annotation_log.csv", names=["Time", "Ticker", "Strategy", "Conf", "Reason"])
    st.dataframe(ann.tail(10), use_container_width=True)
except Exception:
    st.warning("No annotations found yet.")
