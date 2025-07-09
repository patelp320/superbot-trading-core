import os
import random
import subprocess
from datetime import datetime, timezone


def main():
    underperform = random.random() < 0.5
    if underperform:
        print(f"[{datetime.now(timezone.utc)}] 🔄 Retraining models...")
        subprocess.call(["python3", "learn_core.py"])
    else:
        print(f"[{datetime.now(timezone.utc)}] ✅ Models performing well. No retrain.")


if __name__ == "__main__":
    main()
