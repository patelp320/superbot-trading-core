import os
import subprocess
from datetime import datetime, timezone

STRATEGY_DIR = "../strategy"
LOG_FILE = "../logs/error_map.log"
os.makedirs("../logs", exist_ok=True)

for file in os.listdir(STRATEGY_DIR):
    if file.endswith(".py"):
        path = os.path.join(STRATEGY_DIR, file)
        try:
            print(f"🚀 Running {file}")
            subprocess.check_output(["python3", path], stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            with open(LOG_FILE, "a") as log:
                log.write(f"[{datetime.now(timezone.utc)}] ❌ {file} failed:\n{e.output.decode()}\n")
            print(f"❌ {file} failed — sending to auto_debugger")
            subprocess.call(["python3", "auto_debugger.py"])

if __name__ == "__main__":
    print("[RUNNER] Executed all modules.")
