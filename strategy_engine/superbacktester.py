import os
import importlib.util
import shutil
import random
from datetime import datetime

STRATEGY_DIR = "../strategy"
LIVE_DIR = "../live_strategies"
os.makedirs(LIVE_DIR, exist_ok=True)


def load_run(path: str):
    spec = importlib.util.spec_from_file_location("strategy", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, "run", lambda: random.uniform(0, 1))


def main():
    results = []
    for file in os.listdir(STRATEGY_DIR):
        if file.endswith(".py"):
            path = os.path.join(STRATEGY_DIR, file)
            run = load_run(path)
            score = run()
            results.append((score, file))
    results.sort(reverse=True)


    log_file = "../logs/strategy_performance.log"
    with open(log_file, "a") as log:
        for score, file in results:
            log.write(f"[{datetime.utcnow()}] {file} score: {round(score,3)}\n")

    # Prune bottom 20% from strategy directory
    if results:
        cutoff = max(1, int(len(results) * 0.2))
        for _, file in results[-cutoff:]:
            try:
                os.remove(os.path.join(STRATEGY_DIR, file))
            except FileNotFoundError:
                pass
    for _, file in results[5:]:
        target = os.path.join(LIVE_DIR, file)
        if os.path.exists(target):
            os.remove(target)
    for _, file in results[:5]:
        shutil.copy(os.path.join(STRATEGY_DIR, file), os.path.join(LIVE_DIR, file))

    print(f"[{datetime.utcnow()}] ⏪ Backtest complete. Top strategies updated.")


if __name__ == "__main__":
    main()
