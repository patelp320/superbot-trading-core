import json
import os

MODULES = ["learn_core", "predict_core", "options_ai", "strategy_writer", "self_runner", "ibkr_executor_sim"]

LOG_FILE = "log_status.json"

def load_last_status():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            return json.load(f).get("last_module", None)
    return None

def save_status(module_name):
    with open(LOG_FILE, "w") as f:
        json.dump({"last_module": module_name}, f)

def resume():
    last = load_last_status()
    if last:
        try_idx = MODULES.index(last) + 1
    else:
        try_idx = 0

    for module in MODULES[try_idx:]:
        print(f"[RECOVERY] Running {module}...")
        try:
            __import__(module).run()
            save_status(module)
        except Exception as e:
            print(f"❌ {module} failed:", e)
            break
