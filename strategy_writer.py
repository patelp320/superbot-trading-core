import os
from datetime import datetime
import random

STRATEGY_DIR = "../strategy"
LOG_FILE = "../logs/self_written.log"
os.makedirs(STRATEGY_DIR, exist_ok=True)
os.makedirs("../logs", exist_ok=True)

def generate_strategy(name):
    templates = [
        "0DTE iron condor on QQQ/SPY every Thu/Fri",
        "High-IV put credit spread on earnings week",
        "Gap-and-Go penny stock scalp",
        "Mean reversion short on parabolic move"
    ]
    template = random.choice(templates)
    code = f"""
# Auto-generated strategy: {name}
import random
from datetime import datetime

def run():
    score = random.uniform(0.1, 0.8)
    print(f"[{{datetime.utcnow()}}] 🚀 {name} ({template}): mock alpha score = {{round(score, 3)}}")
    return score
"""
    return code

timestamp = datetime.utcnow().strftime("%H%M%S")
strat_name = f"alpha_{timestamp}"
file_name = os.path.join(STRATEGY_DIR, f"{strat_name}.py")

with open(file_name, "w") as f:
    f.write(generate_strategy(strat_name))

with open(LOG_FILE, "a") as log:
    log.write(f"[{datetime.utcnow()}] 🧠 Created new strategy: {strat_name}.py\n")

print(f"✅ New strategy written: {strat_name}.py")

if __name__ == "__main__":
    timestamp = datetime.utcnow().strftime("%H%M%S")
    strat_name = f"alpha_{timestamp}"
    file_name = os.path.join("../strategy", f"{strat_name}.py")
    with open(file_name, "w") as f:
        f.write(generate_strategy(strat_name))
    print(f"✅ New strategy written: {strat_name}.py")
