# Superbot Trading Core

This repository contains experimental trading bots and utilities.

## Running Tests

Install dependencies and execute the unit tests using Python's built-in test runner:

```bash
pip install -r requirements.txt
python -m unittest discover -s tests
```

## New Features
 <<<<<<< xk94hs-codex/upgrade-trading-bot-with-advanced-features
=======

- **Market Anomaly Detector** – checks for trading halts or flash crash conditions using `market_anomaly_detector.py`.
- **Broker Failover** – `ibkr_executor_sim.py` now selects between IBKR, Alpaca, or a paper broker using `broker_failover.py`.
 <<<<<<< i1gxvq-codex/upgrade-trading-bot-with-advanced-features
- **Advanced Ensemble** – `ai_modules/multi_model_ensemble.py` now mixes XGBoost, LSTM, CNN, CatBoost, and Transformer models with regime-based weighting.
- **Reinforcement Learning Framework** – `ai_modules/reinforcement_learner.py` provides PPO training and offline RL stubs.
=======
 >>>>>>> main

 >>>>>>> main

- **Market Anomaly Detector** – checks for trading halts or flash crash conditions using `market_anomaly_detector.py`.
- **Broker Failover** – `ibkr_executor_sim.py` now selects between IBKR, Alpaca, or a paper broker using `broker_failover.py`.
- **Advanced Ensemble** – `ai_modules/multi_model_ensemble.py` now mixes XGBoost, LSTM, CNN, CatBoost, and Transformer models with regime-based weighting.
- **Reinforcement Learning Framework** – `ai_modules/reinforcement_learner.py` provides PPO training and offline RL stubs.


- **Alt Data Ingest** – `ai_modules/alt_data_ingest.py` collects news from Benzinga, Unusual Whales, WhaleStream and FinBrain.
- **Dark Pool & Options Flow** – `ai_modules/dark_pool_flow.py` flags unusual dark pool prints and options activity.
- **Social Alpha Integration** – `ai_modules/social_alpha.py` scrapes r/WallStreetBets and StockTwits for trending tickers.
