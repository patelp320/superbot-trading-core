import json
import time


def tokenize_strategy(file):
    with open(file, "r") as f:
        strat = json.load(f)

    content = f"""
# Auto-generated Strategy
def run(data):
    if {strat['entry_signal']}:
        if {strat['exit']}:
            return "EXIT"
        elif {strat['stop']}:
            return "STOP"
        else:
            return "HOLD"
    return "NO ENTRY"
"""

    fname = f"strategies/alpha_{int(time.time())}.py"
    with open(fname, "w") as f:
        f.write(content)
    print(f"[TOKENIZER] ✅ Strategy saved to {fname}")
