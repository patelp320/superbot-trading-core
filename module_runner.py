import os
import subprocess
from datetime import datetime, timezone

STRATEGY_DIR = "../strategy"
LOG_FILE = "../logs/module_runner.log"
WHITELIST = ["options_ai.py", "penny_ai.py"]  # Add more here

os.makedirs("../logs", exist_ok=True)

def log(msg):
    with open(LOG_FILE, "a") as f:
        entry = f"[{datetime.now(timezone.utc).isoformat()}] {msg}\n"
        print(entry.strip())
        f.write(entry)

for file in os.listdir(STRATEGY_DIR):
    if file.endswith(".py") and file in WHITELIST:
        try:
            log(f"🚀 Running {file}")
            result = subprocess.run(["python3", os.path.join(STRATEGY_DIR, file)], capture_output=True, text=True)
            log(f"✅ Output:\n{result.stdout}")
            if result.stderr:
                log(f"⚠️ Error:\n{result.stderr}")
        except Exception as e:
            log(f"❌ Failed to run {file}: {e}")
