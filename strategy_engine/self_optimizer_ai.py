import random
import os
from datetime import datetime
from strategy_writer import generate_strategy

STRATEGY_DIR = "../strategy"


def mutate_strategy(name: str):
    code = generate_strategy(name)
    path = os.path.join(STRATEGY_DIR, f"{name}.py")
    with open(path, "w") as f:
        f.write(code)


def main():
    for i in range(5):
        mutate_strategy(f"ga_{i}_{int(random.random()*1000)}")
    print(f"[{datetime.utcnow()}] 🤖 Strategies mutated.")


if __name__ == "__main__":
    main()
