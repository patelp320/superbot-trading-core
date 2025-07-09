import streamlit as st
import json
import os
from performance_tracker import summary
from alpha_discovery import discover_tickers
from compliance_guard import is_blocked
from auto_updater import run_update
from strategy_mutator import mutate_all

st.set_page_config(layout="wide")
st.title("📊 Superbot Dashboard")

# Mode Switch
st.subheader("⚙️ Trading Mode")
mode = st.radio("Select mode:", ["paper", "live"])
if st.button("Save Mode"):
    with open("config.json", "w") as f:
        json.dump({"mode": mode}, f)
    st.success(f"✅ Mode saved: {mode}")

# PnL Tracking
st.subheader("💰 PnL Summary")
summary()

# Strategy + Model Reload
st.subheader("🔄 Refresh Core")
if st.button("Run Auto Updater"):
    run_update()
    st.success("✅ Updated models & strategies")

if st.button("Mutate Strategies"):
    mutate_all()
    st.success("✅ Mutation complete")

# Alpha Suggestions
st.subheader("📈 Alpha Discovery")
if st.button("Discover Tickers"):
    tickers = discover_tickers()
    st.write("Suggested:", tickers)

# Compliance Check
st.subheader("🔒 Compliance Check")
ticker_check = st.text_input("Enter ticker to check")
price = st.number_input("Price", value=1.0)
days = st.slider("Option expiry in days", 0, 30, 7)
if st.button("Check Compliance"):
    if is_blocked(ticker_check.upper(), price, days):
        st.error("❌ Trade Blocked")
    else:
        st.success("✅ Trade Allowed")
