import os
import pickle
import importlib

model_cache = {}
strategy_cache = {}

def update_models():
    for file in os.listdir("models"):
        if file.endswith(".pkl"):
            ticker = file.replace("_model.pkl", "")
            with open(f"models/{file}", "rb") as f:
                model_cache[ticker] = pickle.load(f)
    print(f"[UPDATER] ✅ Reloaded {len(model_cache)} models")

def update_strategies():
    for file in os.listdir("strategies"):
        if file.startswith("alpha_") and file.endswith(".py"):
            name = file[:-3]
            strategy_cache[name] = importlib.import_module(f"strategies.{name}")
    print(f"[UPDATER] ✅ Reloaded {len(strategy_cache)} strategies")

def run_update():
    update_models()
    update_strategies()
