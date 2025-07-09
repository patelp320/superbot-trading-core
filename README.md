# Superbot Trading Core

This repository contains experimental trading bots and utilities.

## Running Tests

Install dependencies and execute the unit tests using pytest:

```bash
pip install -r requirements.txt
pytest tests/
```

## New Features

- **Market Anomaly Detector** – checks for trading halts or flash crash conditions using `market_anomaly_detector.py`.
- **Broker Failover** – `ibkr_executor_sim.py` selects between IBKR, Alpaca, or a paper broker using `broker_failover.py`.
- **Advanced Ensemble** – `ai_modules/multi_model_ensemble.py` mixes XGBoost, LSTM, CNN, CatBoost, and Transformer models with regime-based weighting.
- **Reinforcement Learning Framework** – `ai_modules/reinforcement_learner.py` provides PPO training and offline RL stubs.
- **Alt Data Ingest** – `ai_modules/alt_data_ingest.py` collects news from Benzinga, Unusual Whales, WhaleStream and FinBrain.
- **Dark Pool & Options Flow** – `ai_modules/dark_pool_flow.py` flags unusual dark pool prints and options activity.
- **Social Alpha Integration** – `ai_modules/social_alpha.py` scrapes r/WallStreetBets and StockTwits for trending tickers.
- **Penny-Options Integration** – `penny_options_bot.py` cross-checks penny watchlists with options filters.
- **Options Intelligence Toolkit** – `flow_scanner.py`, `delta_filter.py`, `smart_roller.py` and more provide scanning, delta selection, IV and POP filters, and ladder building.
- **GUI Control Panel** – `superbot_gui.py` offers a Tkinter interface for managing credentials and viewing mock trade ideas.
- **Streamlit Dashboard** – `gui.py` runs in the browser for viewing predictions and trade logs.
- **Equity Curve Watchdog** – `equity_curve_watchdog.py` pauses trading if the drawdown exceeds a configurable threshold.

## Running the Web Dashboard in Docker

Build the Docker image and start the Streamlit dashboard:

```bash
docker build -t superbot-auto:latest .
docker run -it --rm -p 8501:8501 superbot-auto:latest
```

Then open <http://localhost:8501> in your browser to view the dashboard.
