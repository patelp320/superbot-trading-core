import os
import time
import re

STRATEGY_DIR = "./strategies"


def mutate_strategy(file_path: str) -> str:
    """Create a mutated copy of the strategy file."""
    with open(file_path, "r") as f:
        code = f.read()

    # Very naive parameter tweak: increase threshold by 10%
    code = re.sub(r"threshold\s*=\s*(\d+\.?\d*)", lambda m: f"threshold = {float(m.group(1)) * 1.1:.2f}", code)

    new_filename = f"{STRATEGY_DIR}/alpha_{int(time.time())}.py"
    with open(new_filename, "w") as f:
        f.write(code)

    print(f"✅ Mutated strategy saved as {new_filename}")
    return new_filename


def mutate_all():
    for fname in os.listdir(STRATEGY_DIR):
        if fname.startswith("alpha_") and fname.endswith(".py"):
            mutate_strategy(os.path.join(STRATEGY_DIR, fname))
