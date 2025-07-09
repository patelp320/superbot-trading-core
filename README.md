# Superbot Trading Core

This repository contains experimental trading bots and utilities.

## Running Tests

Install dependencies and execute the unit tests using Python's built-in test runner:

```bash
pip install -r requirements.txt
python -m unittest discover -s tests
```

## New Features

- **Market Anomaly Detector** – checks for trading halts or flash crash conditions using `market_anomaly_detector.py`.
- **Broker Failover** – `ibkr_executor_sim.py` now selects between IBKR, Alpaca, or a paper broker using `broker_failover.py`.
 <<<<<<< i1gxvq-codex/upgrade-trading-bot-with-advanced-features
- **Advanced Ensemble** – `ai_modules/multi_model_ensemble.py` now mixes XGBoost, LSTM, CNN, CatBoost, and Transformer models with regime-based weighting.
- **Reinforcement Learning Framework** – `ai_modules/reinforcement_learner.py` provides PPO training and offline RL stubs.
=======
 >>>>>>> main


